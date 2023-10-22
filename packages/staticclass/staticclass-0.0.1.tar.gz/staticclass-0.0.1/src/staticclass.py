from types import FunctionType


def _static_new(cls):
    """
    A blank for creating a __new__ method with an exception.
    """
    raise StaticError()

def _set_static_new_to_dict(dict_):
    """
    Allow to set a blank method to dict.
    """
    dict_["__new__"] = _static_new

def _set_static_new_to_cls(cls):
    """
    Allow to set a blank method to class.
    """
    setattr(cls, "__new__", _static_new)


class StaticError(BaseException):
    """
    Any type of error associated with a static class.
    """
    pass


class StaticMeta(type):
    """
    The basis of static classes.
    """
    def __new__(cls, name, bases, namespace, /, **kwargs):
        _set_static_new_to_dict(namespace)
        static_namespace = StaticMeta._static_namespace(namespace)
        cls = super().__new__(cls, name, bases, static_namespace, **kwargs)
        return cls

    def _static_namespace(namespace: dict):
        static_namespace = namespace.copy()
        for name, attr in static_namespace.items():
            if isinstance(attr, FunctionType):
                static_namespace[name] = staticmethod(attr)
        return static_namespace


class Static(metaclass=StaticMeta):
    """
    Helper class that provides a standard way\n
    to create an Static using inheritance.
    """
    __slots__ = ()


def _static_class(cls: type):
    """
    Replacement of inheritance as a decorator.
    """
    namespace = cls.__dict__
    for name, attr in namespace.items():
        if isinstance(attr, FunctionType):
            setattr(cls, name, staticmethod(attr))
    _set_static_new_to_cls(cls)
    return cls

static_class = _static_class
staticclass = _static_class
staticClass = _static_class