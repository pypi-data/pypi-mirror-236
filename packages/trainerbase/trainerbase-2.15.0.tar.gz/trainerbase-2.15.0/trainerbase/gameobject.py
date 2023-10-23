from abc import ABC, abstractmethod
from typing import Self, override
from uuid import uuid4

from trainerbase.memory import ConvertibleToAddress, ensure_address, pm


class GameObject[PymemType, TrainerBaseType](ABC):
    DPG_TAG_PREFIX = "object__"
    DPG_TAG_POSTFIX_IS_FROZEN = "__frozen"
    DPG_TAG_POSTFIX_GETTER = "__getter"
    DPG_TAG_POSTFIX_SETTER = "__setter"

    updated_objects: list[Self] = []

    @staticmethod
    @abstractmethod
    def pm_read(address: int) -> PymemType:
        pass

    @staticmethod
    @abstractmethod
    def pm_write(address: int, value: PymemType) -> None:
        pass

    def __init__(
        self,
        address: ConvertibleToAddress,
        frozen: TrainerBaseType | None = None,
    ):
        GameObject.updated_objects.append(self)

        self.address = ensure_address(address)
        self.frozen = frozen

        dpg_tag = f"{GameObject.DPG_TAG_PREFIX}{uuid4()}"
        self.dpg_tag_frozen = f"{dpg_tag}{GameObject.DPG_TAG_POSTFIX_IS_FROZEN}"
        self.dpg_tag_getter = f"{dpg_tag}{GameObject.DPG_TAG_POSTFIX_GETTER}"
        self.dpg_tag_setter = f"{dpg_tag}{GameObject.DPG_TAG_POSTFIX_SETTER}"

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}"
            f" at {hex(self.address.resolve())}:"
            f" value={self.value},"
            f" frozen={self.frozen},"
            f" dpg_tag_frozen={self.dpg_tag_frozen},"
            f" dpg_tag_getter={self.dpg_tag_getter}"
            f" dpg_tag_setter={self.dpg_tag_setter}"
            ">"
        )

    def after_read(self, value: PymemType) -> TrainerBaseType:
        return value  # type: ignore

    def before_write(self, value: TrainerBaseType) -> PymemType:
        return value  # type: ignore

    @property
    def value(self) -> TrainerBaseType:
        return self.after_read(self.pm_read(self.address.resolve()))

    @value.setter
    def value(self, new_value: TrainerBaseType):
        self.pm_write(self.address.resolve(), self.before_write(new_value))


class GameFloat(GameObject[float, float]):
    pm_read = pm.read_float  # type: ignore
    pm_write = pm.write_float

    @override
    def before_write(self, value):
        return float(value)


class GameDouble(GameObject[float, float]):
    pm_read = pm.read_double  # type: ignore
    pm_write = pm.write_double

    @override
    def before_write(self, value):
        return float(value)


class GameByte(GameObject[bytes, int]):
    @staticmethod
    @override
    def pm_read(address: int) -> bytes:
        return pm.read_bytes(address, length=1)

    @staticmethod
    @override
    def pm_write(address: int, value: bytes) -> None:
        pm.write_bytes(address, value, length=1)

    @override
    def before_write(self, value: int) -> bytes:
        return value.to_bytes(length=1, byteorder="little")

    @override
    def after_read(self, value: bytes) -> int:
        return int.from_bytes(value, byteorder="little")


class GameInt(GameObject[int, int]):
    pm_read = pm.read_int  # type: ignore
    pm_write = pm.write_int


class GameShort(GameObject[int, int]):
    pm_read = pm.read_short  # type: ignore
    pm_write = pm.write_short


class GameLongLong(GameObject[int, int]):
    pm_read = pm.read_longlong  # type: ignore
    pm_write = pm.write_longlong


class GameUnsignedInt(GameObject[int, int]):
    pm_read = pm.read_uint  # type: ignore
    pm_write = pm.write_uint


class GameUnsignedShort(GameObject[int, int]):
    pm_read = pm.read_ushort  # type: ignore
    pm_write = pm.write_ushort


class GameUnsignedLongLong(GameObject[int, int]):
    pm_read = pm.read_ulonglong  # type: ignore
    pm_write = pm.write_ulonglong


class GameBool(GameObject[bool, bool]):
    pm_read = pm.read_bool  # type: ignore
    pm_write = pm.write_bool
