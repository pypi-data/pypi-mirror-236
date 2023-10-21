# Copyright (c) 2022 VMware, Inc. All Rights Reserved.
import datetime

from model_manager.common.serializable import Serializable


class VersionedRef(Serializable):
    def __init__(self, name: str, version: str):
        self.name = name
        self.version = version

    def __repr__(self):
        params = ", ".join(
            "{}={}".format(key, repr(value)) for key, value in self.__dict__.items() if not key.startswith("_"))
        return "{cls_name}({params})".format(cls_name=self.__class__.__name__, params=params)

    def __str__(self):
        return "{name}@{version}".format(name=self.name, version=self.version)

    def __eq__(self, other):
        if not other:
            return False
        if not isinstance(other, self.__class__):
            return False
        return self.name == other.name and self.version == other.version

    def __hash__(self):
        return hash(str(self))

    @classmethod
    def parse(cls, ref: str):
        name, version = ref.split("@")
        return cls(name=name, version=version)


class BaseMetadata(Serializable):
    TIME_FORMAT = "%Y-%m-%d %H:%M:%S"

    def __init__(self, name:str, org_id: str=None, version: str=None, tags: dict=None, creation_time: str=None):
        self.name = name
        self.org_id = 'vmware' if org_id is None else org_id
        self.tags = {} if tags is None else tags
        self.version = version
        if creation_time is not None:
            self.creation_time = creation_time
        else:
            self.creation_time = BaseMetadata.date_to_str(datetime.datetime.utcnow())

    @staticmethod
    def date_to_str(date: datetime.datetime) -> str:
        return date.strftime(BaseMetadata.TIME_FORMAT)

    @staticmethod
    def parse_date(s: str) -> datetime.datetime:
        return datetime.datetime.strptime(s, BaseMetadata.TIME_FORMAT)
