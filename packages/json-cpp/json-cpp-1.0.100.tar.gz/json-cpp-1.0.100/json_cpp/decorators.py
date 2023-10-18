def _use_self_or_cls(funct):
    from inspect import signature, _empty
    s = signature(funct)
    b = "self" in s.parameters and s.parameters["self"].annotation is _empty
    if b:
        return b
    b = "cls" in s.parameters and s.parameters["cls"].annotation is _empty
    if b:
        return b
    b = "self_or_cls" in s.parameters and s.parameters["self_or_cls"].annotation is _empty
    return b


def json_force_parameter_type_function(funct):
    def decorated(*args, **kwargs):
        from inspect import signature
        from .json_object import JsonObject, JsonList
        if args:
            args = list(args)
        parameters = signature(funct).parameters
        for pi, p in enumerate(parameters):
            if issubclass(parameters[p].annotation, JsonObject) and parameters[p].annotation is not JsonObject:
                if p in kwargs and isinstance(kwargs[p], JsonObject):
                    kwargs[p] = kwargs[p].into(parameters[p].annotation)
                if pi < len(args):
                    args.insert(pi, args.pop(pi).into(parameters[p].annotation))
            elif issubclass(parameters[p].annotation, JsonList) and parameters[p].annotation is not JsonList:
                if p in kwargs and isinstance(kwargs[p], JsonList):
                    kwargs[p] = kwargs[p].into(parameters[p].annotation)
                if pi < len(args):
                    args.insert(pi, args.pop(pi).into(parameters[p].annotation))
            elif p in kwargs and type(kwargs[p]) is str and parameters[p].annotation is not str:
                kwargs[p] = parameters[p].annotation(kwargs[p])
                if pi < len(args):
                    args.insert(pi, args.pop(pi).into(parameters[p].annotation))
        return funct(*args, **kwargs)
    return decorated


def json_force_parameter_type_method(funct):
    def decorated(self_or_cls, *args, **kwargs):
        from inspect import signature, _empty
        from .json_object import JsonObject, JsonList
        if args:
            args = list(args)
        parameters = signature(funct).parameters
        for pi, p in enumerate(parameters):
            if parameters[p].annotation is _empty:
                continue #not type was specified, so there is no type to enforce
            if issubclass(parameters[p].annotation, JsonObject):
                if p in kwargs:
                    if type(kwargs[p]) is JsonObject and parameters[p].annotation is not JsonObject:
                        kwargs[p] = kwargs[p].into(parameters[p].annotation)
                    elif isinstance(kwargs[p], str):
                        kwargs[p] = parameters[p].annotation.parse(kwargs[p])
                if pi < len(args):
                    if type(kwargs[p]) is JsonObject and parameters[p].annotation is not JsonObject:
                        args.insert(pi, args.pop(pi).into(parameters[p].annotation))
                    elif type(kwargs[p]) is str:
                        args.insert(pi, parameters[p].annotation.parse(args.pop(pi)))
            elif issubclass(parameters[p].annotation, JsonList):
                if p in kwargs:
                    if type(kwargs[p]) is JsonList and parameters[p].annotation is not JsonList:
                        kwargs[p] = kwargs[p].into(parameters[p].annotation)
                    elif isinstance(kwargs[p], str):
                        kwargs[p] = parameters[p].annotation.parse(kwargs[p])
                if pi < len(args):
                    if type(kwargs[p]) is JsonList and parameters[p].annotation is not JsonList:
                        args.insert(pi, args.pop(pi).into(parameters[p].annotation))
                    elif type(kwargs[p]) is str:
                        args.insert(pi, parameters[p].annotation.parse(args.pop(pi)))
            else:
                if p in kwargs:
                    if type(kwargs[p]) is not parameters[p].annotation:
                        kwargs[p] = parameters[p].annotation(kwargs[p])
                if pi < len(args):
                    if type(kwargs[p]) is not parameters[p].annotation:
                        args.insert(pi, parameters[p].annotation(args.pop(pi)))
        return funct(self_or_cls, *args, **kwargs)
    return decorated


def json_force_parameter_type(funct):
    if _use_self_or_cls(funct):
        return json_force_parameter_type_method(funct)
    else:
        return json_force_parameter_type_function(funct)


def json_parameters_function(funct):
    def decorated(json_object):
        from .json_object import JsonObject
        if not isinstance(json_object, JsonObject):
            raise TypeError("Parameter must be JsonObject instance")
        p = json_object.to_dict()
        return funct(**p)
    return decorated


def json_parameters_method(funct):
    from inspect import signature
    def decorated(self_or_cls, json_object):
        from .json_object import JsonObject
        if not isinstance(json_object, JsonObject):
            raise TypeError("Parameter must be JsonObject instance")
        p = json_object.to_dict()
        return funct(self_or_cls, **p)

    return decorated


def json_parameters(funct):
    if _use_self_or_cls(funct):
        return json_parameters_method(funct)
    else:
        return json_parameters_function(funct)


def json_parse(json_object_type=None):
    def decorator(funct):
        from .json_object import JsonObject
        if _use_self_or_cls(funct):
            if json_object_type:
                def decorated(self_or_cls, json_string: str):
                    return funct(self_or_cls, json_object_type.parse(json_string))
            else:
                def decorated(self_or_cls, json_string: str):
                    return funct(self_or_cls, JsonObject.load(json_string))
        else:
            if json_object_type:
                def decorated(json_string: str):
                    return funct(json_object_type.parse(json_string))
            else:
                def decorated(json_string: str):
                    return funct(JsonObject.load(json_string))
        return decorated
    from .json_object import JsonObject
    if not type(json_object_type) is type:
        funct = json_object_type
        json_object_type = None
        return decorator(funct)
    return decorator


class classorinstancemethod(classmethod):

    def __get__(self, instance, type_):
        descr_get = super().__get__ if instance is None else self.__func__.__get__
        return descr_get(instance, type_)
