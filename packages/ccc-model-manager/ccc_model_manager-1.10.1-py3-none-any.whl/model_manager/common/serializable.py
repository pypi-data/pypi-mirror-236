# Copyright (c) 2022 VMware, Inc. All Rights Reserved.

import typing
import numpy as np
import enum
from collections.abc import Iterable
import inspect
import logging

import six


_logger = logging.getLogger(__name__)


class Serializable(object):
    """
    Mixin to handle serializing/deserializing objects to/from dictionary. It provides default implementations of the
    methods that should work in most of the cases.
    """
    def serialize(self) -> dict:
        """Serialize the object to a dictionary"""
        data = {k: self._serialize_item(v) for k, v in self.__dict__.items() if not k.startswith("_")}
        return data

    @staticmethod
    def _serialize_item(v):
        if isinstance(v, Serializable):
            return v.serialize()
        elif isinstance(v, np.ndarray):
            return v.tolist()
        elif isinstance(v, dict):
            return {Serializable._serialize_item(k): Serializable._serialize_item(el) for k, el in v.items()}
        elif isinstance(v, (tuple, list, set)):
            return [Serializable._serialize_item(el) for el in v]
        elif isinstance(v, enum.IntEnum):
            return v.name
        elif isinstance(v, enum.Enum):
            return v.value
        else:
            return v

    @classmethod
    def _get_arg_types(cls):
        signature = inspect.signature(cls.__init__)
        needs_parent_types = any(param.kind == inspect.Parameter.VAR_KEYWORD for param in signature.parameters.values())
        types = typing.get_type_hints(cls.__init__)
        if needs_parent_types:
            parent_classes = cls.mro()[1:]  # The first one is the current class
            if len(parent_classes) > 0:
                immediate_parent = parent_classes[0]
                if issubclass(immediate_parent, Serializable):
                    types.update(immediate_parent._get_arg_types())
        return types

    @classmethod
    def deserialize(cls, data: dict):
        """Deserialize the object from a dictionary"""
        if data is None:
            raise ValueError("data is None")
        types = cls._get_arg_types()
        params = None
        for arg, arg_type in types.items():
            if arg not in data:
                # If the value is not present avoid setting to None to ensure defaults are enforced
                continue
            f = cls._get_deserialization_f(arg_type)
            if not f:
                # If there is no deserialization function, we just preserve the value
                continue
            if not params:
                params = data.copy()
            params[arg] = f(data[arg])
        if params:
            data = params
        try:
            return cls(**data)
        except Exception:
            _logger.exception(f"Error deserializing {cls.__name__} with data {data}")
            raise

    def __str__(self):
        return "{cls_name}({args})".format(cls_name=self.__class__.__name__, args=", ".join([f"{key}={value}" for key, value in self.__dict__.items() if not key.startswith("_")]))

    def __repr__(self):
        return str(self)

    @classmethod
    def _get_deserialization_f(cls, arg_type) -> typing.Optional[typing.Callable]:
        """
        Returns a function that can be used to deserialize value of the provided type.
        :param arg_type:
        :return: Function that accepts a single argument - the value to deserialize or None if deserialization is not needed
        """
        if arg_type is type(None):  # noqa
            return None
        if arg_type is np.ndarray:
            return cls._optional(np.array)
        if arg_type is set or arg_type is tuple:
            return cls._optional(arg_type)
        if isinstance(arg_type, six.class_types) and issubclass(arg_type, Serializable):
            return cls._optional(arg_type.deserialize)
        if isinstance(arg_type, six.class_types) and issubclass(arg_type, enum.IntEnum):
            return cls._optional(lambda x: arg_type[x])
        if isinstance(arg_type, six.class_types) and issubclass(arg_type, enum.Enum):
            return cls._optional(arg_type)
        generic_type = Serializable._get_type(arg_type)
        if (generic_type is list) or (generic_type is typing.List) or (generic_type is Iterable):
            if len(arg_type.__args__) == 0:
                return None
            el_f = cls._get_deserialization_f(arg_type.__args__[0])
            if not el_f:
                return None
            return cls._optional(lambda v: [el_f(el) if el_f else el for el in v])
        if (generic_type is set) or (generic_type is typing.Set):
            if len(arg_type.__args__) == 0:
                return cls._optional(set)
            el_f = cls._get_deserialization_f(arg_type.__args__[0])
            return cls._optional(lambda v: {el_f(el) if el_f else el for el in v})
        if (generic_type is tuple) or (generic_type is typing.Tuple):
            if len(arg_type.__args__) == 0:
                return cls._optional(list)
            el_fs = [cls._get_deserialization_f(el_arg_type) for el_arg_type in arg_type.__args__ if el_arg_type != Ellipsis]
            return cls._optional(cls._deserialize_tuple_f(el_fs))
        if (generic_type is dict) or (generic_type is typing.Dict):
            k_arg_type, el_arg_type = arg_type.__args__
            k_f = cls._get_deserialization_f(k_arg_type)
            el_f = cls._get_deserialization_f(el_arg_type)
            if not (k_f or el_f):
                return None
            return cls._optional(lambda v: {(k_f(k) if k_f else k): (el_f(el) if el_f else el) for k, el in v.items()})
        if generic_type is typing.Union:
            types = arg_type.__args__
            if len(types) == 2 and type(None) in types:
                # can't use isinstance on generic types, but only want to compare to NoneType
                el_arg_type = types[0] if types[1] is type(None) else types[0]  # noqa
                return cls._get_deserialization_f(el_arg_type)
        return None

    @classmethod
    def _deserialize_tuple_f(cls, el_fs):
        def get_el_f(i):
            el_f = el_fs[i] if i < len(el_fs) else el_fs[-1]
            return el_f if el_f else lambda v: v

        def deserialize(v):
            return tuple([get_el_f(i)(el) for i, el in enumerate(v)])
        return deserialize

    @staticmethod
    def _optional(f):
        """
        Function wrapper that check if the argument is json-serializable type and only then applies the function on it.
        :param f:
        :return:
        """
        def safe_invoke(x):
            if not isinstance(x, (int, str, bool, float, list, dict)):
                # Make sure we skip attributes that were deserialized outside
                return x
            return f(x) if x is not None else None

        return safe_invoke

    @staticmethod
    def _get_type(arg_type):
        """
        Returns the generic type of the type hint. Python 3.8 provides similar functionality.
        :param arg_type:
        :return:
        """
        return getattr(arg_type, '__origin__', None)
