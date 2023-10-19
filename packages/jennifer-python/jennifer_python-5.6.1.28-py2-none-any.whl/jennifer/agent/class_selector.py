import sys
import types
import os
from . import atomic_integer
from .util import _log
from jennifer.agent import jennifer_agent


class MethodSelector:

    ALL_PARAMETER = 0
    ARG_PARAMETER_ONLY = 1
    NAMED_PARAMETER_ONLY = 2
    BOTH_PARAMETER = 3
    RETURN_VALUE = 4

    UNDEFINED = 0
    MODULE_FUNCTION = 1
    CLASS_STATIC_METHOD = 2
    CLASS_INSTANCE_METHOD = 4

    PROFILE_NONE = 0
    PROFILE_USER_ID = 1
    PROFILE_GUID = 2
    PROFILE_METHOD = 4

    def __init__(self, text, profile_type, profile_return_value=False):
        self.text = text
        self.profile_module = None
        self.profile_class = None
        self.profile_func_key = None
        self.profile_arg_idx = []
        self.profile_arg_names = []
        self.is_initialized = False
        self.profile_type = profile_type

        if profile_type == MethodSelector.PROFILE_NONE:
            return

        if profile_return_value:
            self.param_mode = MethodSelector.RETURN_VALUE
        else:
            self.param_mode = MethodSelector.ALL_PARAMETER

        self.is_instance = False
        self.original_target_container = None
        self.original_func = None
        self.func_type = MethodSelector.UNDEFINED

        try:
            self.parse_profile_item(text)
        except:
            _log('exception', 'invalid profile item', text)
            pass

    def parse_profile_item(self, item):
        item = str(item).strip()
        items = item.split(' ')
        if len(items) < 2:
            _log('warning', 'invalid profile item', item)
            return

        self.profile_module = items[0].strip()

        class_or_func = items[1].strip().split('.')
        if len(class_or_func) < 2:
            self.profile_func_key, arg_info = MethodSelector.parse_bracket(class_or_func[0].strip())
        else:
            self.profile_class = class_or_func[0].strip()
            if len(self.profile_class) == 0:
                self.profile_class = None
            self.profile_func_key, arg_info = MethodSelector.parse_bracket(class_or_func[1].strip())

        if len(items) >= 3:
            arg_text = MethodSelector.strip_curly_brace(''.join(items[2:]))
            arg_list = arg_text.split(',')
            for arg in arg_list:
                arg = arg.strip()

                try:
                    is_numeric_arg = arg.isnumeric()
                except AttributeError:
                    is_numeric_arg = unicode(arg).isnumeric()

                if arg_info is None:
                    if is_numeric_arg:
                        self.profile_arg_idx.append(int(arg))
                        self.param_mode |= MethodSelector.ARG_PARAMETER_ONLY
                    else:
                        self.profile_arg_names.append(arg)
                        self.param_mode |= MethodSelector.NAMED_PARAMETER_ONLY
                else:
                    if is_numeric_arg:
                        arg_pos = int(arg) - 1
                        if arg_pos >= len(arg_info):
                            arg_pos = arg
                        else:
                            arg_pos = arg_info[arg_pos]

                        if arg_pos.isnumeric():
                            self.profile_arg_idx.append(int(arg))
                            self.param_mode |= MethodSelector.ARG_PARAMETER_ONLY
                        else:
                            self.profile_arg_names.append(arg_pos)
                            self.param_mode |= MethodSelector.NAMED_PARAMETER_ONLY
                    else:
                        self.profile_arg_names.append(arg)
                        self.param_mode |= MethodSelector.NAMED_PARAMETER_ONLY

        self.is_initialized = True

    @staticmethod
    def parse_bracket(text):
        spos = text.find('(')
        if spos == -1:
            return text, None

        function_name = text[0:spos]
        epos = text.find(')Any')
        if epos == -1:
            return function_name, None

        arg_text = text[spos + 1:epos]
        if len(arg_text) == 0:
            return function_name, []

        arg_info = arg_text.split(',')
        return function_name, arg_info

    @staticmethod
    def strip_curly_brace(text):
        return text.strip().strip('{').strip('}')

    def gather_hook_info(self, target_hooking_func_dict):
        import importlib

        try:
            module = importlib.import_module(self.profile_module)
        except Exception as e:
            _log('diagnostics', 'process_dynamic_hook', 'not loaded', self.text)
            return

        target_func = None
        container_dict = None
        class_type = None
        if self.profile_class is not None:
            class_type = module.__dict__.get(self.profile_class, None)
            if class_type is not None:
                container_dict = class_type.__dict__
                target_func = class_type.__dict__.get(self.profile_func_key, None)
                if target_func is not None:
                    self.is_instance = isinstance(target_func, types.FunctionType)
        else:
            container_dict = module.__dict__
            target_func = module.__dict__.get(self.profile_func_key, None)

        if target_func is None:
            _log('diagnostics', 'process_dynamic_hook', self.profile_module, self.profile_func_key)
            return

        self.register_hook_func(target_hooking_func_dict, class_type, container_dict, target_func)

    def register_hook_func(self, target_hooking_func_dict, class_type, container_dict, target_func):
        item_key = str(target_func)
        if item_key in target_hooking_func_dict.keys():
            cur_value = target_hooking_func_dict[item_key]
            cur_value['profile_type'] = cur_value['profile_type'] | self.profile_type
            cur_value[self.profile_type] = {
                'item_text': self.text,
                'param_mode': self.param_mode,
                'arg_idx': self.profile_arg_idx,
                'arg_names': self.profile_arg_names,
            }
        else:
            new_value = {
                'profile_type': self.profile_type,
                'profile_func_key': self.profile_func_key,
                'class_type': class_type,
                'is_instance': self.is_instance,
                'container_dict': container_dict,
                'target_func': target_func,
                self.profile_type: {
                    'item_text': self.text,
                    'param_mode': self.param_mode,
                    'arg_idx': self.profile_arg_idx,
                    'arg_names': self.profile_arg_names,
                },
            }
            target_hooking_func_dict[item_key] = new_value


def append_tuple_to_list(list_inst, tuple_inst, idx=None):
    if idx is None:
        list_inst.extend([str(item) for item in tuple_inst])
    else:
        for order, item in enumerate(tuple_inst):
            if (order + 1) in idx:
                list_inst.append(str(item))


def append_dict_to_list(list_inst, dict_inst, names=None):
    if names is None:
        list_inst.extend([str(value) for key, value in dict_inst.items()])
    else:
        for key, value in dict_inst.items():
            if key in names:
                list_inst.append(str(value))


def get_value_list(param_mode, args, kwargs, arg_idx, arg_names):
    value_list = []

    if param_mode == MethodSelector.ALL_PARAMETER:
        append_tuple_to_list(value_list, args)
        append_dict_to_list(value_list, kwargs)
    else:
        if param_mode | MethodSelector.ARG_PARAMETER_ONLY:
            append_tuple_to_list(value_list, args, idx=arg_idx)

        if param_mode | MethodSelector.NAMED_PARAMETER_ONLY:
            append_dict_to_list(value_list, kwargs, names=arg_names)

    return value_list


def wrap_non_instance_method(org_func, target_hook_info):

    def inner_handler(*args, **kwargs):
        try:
            process_dynamic_pre_method_func(args, kwargs, target_hook_info)
        except:
            pass

        result = org_func(*args, **kwargs)

        try:
            process_dynamic_post_method_func(args, kwargs, target_hook_info, result)
        except:
            pass

        return result

    return inner_handler


def wrap_class_instance_method(org_func, target_hook_info):

    def inner_handler(self, *args, **kwargs):
        try:
            process_dynamic_pre_method_func(args, kwargs, target_hook_info)
        except:
            pass

        result = org_func(self, *args, **kwargs)

        try:
            process_dynamic_post_method_func(args, kwargs, target_hook_info, result)
        except:
            pass

        return result

    return inner_handler


def process_profile_user_id_pre_method_func(args, kwargs, param_mode, arg_idx, arg_names, o):
    if param_mode & MethodSelector.RETURN_VALUE:
        pass
    else:
        user_id_list = get_value_list(param_mode, args, kwargs, arg_idx, arg_names)
        o.set_user_id(''.join(user_id_list))


def process_profile_guid_pre_method_func(args, kwargs, param_mode, arg_idx, arg_names, o):
    if param_mode & MethodSelector.RETURN_VALUE:
        pass
    else:
        user_id_list = get_value_list(param_mode, args, kwargs, arg_idx, arg_names)
        o.set_guid(''.join(user_id_list))


def hook_info_from(target_hook_info, info_id):
    item_info = target_hook_info[info_id]
    return item_info['param_mode'], item_info['arg_idx'], item_info['arg_names']


def process_dynamic_pre_method_func(args, kwargs, target_hook_info):
    profile_type = target_hook_info['profile_type']

    agent = jennifer_agent()
    if agent is None:
        return

    o = agent.current_active_object()
    if o is None:
        return

    if profile_type & MethodSelector.PROFILE_USER_ID:
        (param_mode, arg_idx, arg_names) = hook_info_from(target_hook_info, MethodSelector.PROFILE_USER_ID)
        process_profile_user_id_pre_method_func(args, kwargs, param_mode, arg_idx, arg_names, o)

    if profile_type & MethodSelector.PROFILE_GUID:
        (param_mode, arg_idx, arg_names) = hook_info_from(target_hook_info, MethodSelector.PROFILE_GUID)
        process_profile_guid_pre_method_func(args, kwargs, param_mode, arg_idx, arg_names, o)


def process_dynamic_post_method_func(args, kwargs, target_hook_info, return_value):
    profile_type = target_hook_info['profile_type']

    agent = jennifer_agent()
    if agent is None:
        return

    o = agent.current_active_object()
    if o is None:
        return

    if profile_type & MethodSelector.PROFILE_USER_ID:
        (param_mode, arg_idx, arg_names) = hook_info_from(target_hook_info, MethodSelector.PROFILE_USER_ID)
        if param_mode & MethodSelector.RETURN_VALUE:
            o.set_user_id(str(return_value))

    if profile_type & MethodSelector.PROFILE_GUID:
        (param_mode, arg_idx, arg_names) = hook_info_from(target_hook_info, MethodSelector.PROFILE_GUID)
        if param_mode & MethodSelector.RETURN_VALUE:
            o.set_guid(str(return_value))


class ClassSelector:

    def __init__(self, text_list, profile_type, profile_return_value=False):
        self.method_list = []
        self.profile_type = profile_type

        if text_list is None or len(text_list) == 0:
            return

        if isinstance(text_list, list) is False:
            return

        for text in text_list:
            parsed_item = MethodSelector(text, profile_type, profile_return_value)
            if parsed_item is None:
                continue
            self.method_list.append(parsed_item)

    def preprocess_hook(self, target_hooking_func_dict):
        for method in self.method_list:
            try:
                method.gather_hook_info(target_hooking_func_dict)
            except Exception as e:
                _log('exception', 'preprocess_hook', method.text, e)

    @staticmethod
    def unhook_func(target_hook_info):
        try:
            original_func = target_hook_info['original_func']
            if original_func is None:
                return

            original_target_container = target_hook_info['original_target_container']
            if original_target_container is None:
                return

            func_type = target_hook_info['func_type']
            profile_func_key = target_hook_info['profile_func_key']

            if func_type == MethodSelector.MODULE_FUNCTION:
                original_target_container[profile_func_key] = original_func
            elif func_type == MethodSelector.CLASS_STATIC_METHOD:
                setattr(original_target_container, profile_func_key, staticmethod(original_func))
            elif func_type == MethodSelector.CLASS_INSTANCE_METHOD:
                setattr(original_target_container, profile_func_key, original_func)
        except Exception as e:
            _log('exception', 'unhook_func', original_func, e)

    @staticmethod
    def hook_func(target_func_name, target_hook_info):
        try:
            container_dict = target_hook_info['container_dict']
            target_func = target_hook_info['target_func']
            target_func_text = target_func_name
            profile_func_key = target_hook_info['profile_func_key']
            is_instance = target_hook_info['is_instance']
            class_type = target_hook_info['class_type']

            func_type = None

            if is_instance:
                func_type = MethodSelector.CLASS_INSTANCE_METHOD
                if target_func_text.find('wrap_class_instance_method.<locals>.handler') != -1:
                    return False

                setattr(class_type, profile_func_key, wrap_class_instance_method(target_func, target_hook_info))

                target_hook_info['original_target_container'] = class_type
                target_hook_info['original_func'] = target_func

                _log('diagnostics', 'hook_func.instance_method', target_func_text)
            else:
                if isinstance(target_func, staticmethod):
                    func_type = MethodSelector.CLASS_STATIC_METHOD
                    if target_func_text.find('wrap_class_static_method.<locals>.handler') != -1:
                        return False

                    setattr(class_type, profile_func_key,
                            staticmethod(wrap_non_instance_method(target_func.__func__, target_hook_info)))

                    target_hook_info['original_target_container'] = class_type
                    target_hook_info['original_func'] = target_func.__func__

                    _log('diagnostics', 'hook_func.static_method', target_func_text)
                else:
                    func_type = MethodSelector.MODULE_FUNCTION
                    if target_func_text.find('wrap_global_function.<locals>.handler') != -1:
                        return False

                    target_hook_info['original_target_container'] = container_dict
                    target_hook_info['original_func'] = target_func
                    container_dict[profile_func_key] = wrap_non_instance_method(target_func, target_hook_info)

                    _log('diagnostics', 'hook_func.module_func', target_func_text)

            target_hook_info['func_type'] = func_type
        except Exception as e:
            _log('exception', 'hook_func', target_func_name, e)

        return True
