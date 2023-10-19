from enum import Enum
from pydantic import BaseModel, field_validator, Field
from typing_extensions import Annotated

# Both registers will start at index = 1
NODE_REGISTER = set([])
ELEMENT_REGISTER = set([])


def register(id: int, register: set[int]):
    # if id in register:
    #     varname = f"{register=}".split("=")[0]
    #     raise ValueError(f"id: {id} was already registered in {varname}")
    register.add(id)


class NodeBase(BaseModel):
    id: Annotated[int | None, Field(validate_default=True, frozen=True)] = None

    @field_validator("id")
    def set_id_now(cls, v):
        try:
            id = v or max(NODE_REGISTER) + 1
        except ValueError:
            id = 1
        register(id, NODE_REGISTER)
        return id


class ElementType(Enum):
    tube = "tube"
    conicaltube = "conicaltube"
    cuboid = "cuboid"
    cone = "cone"


class PolymorphicBaseElement(BaseModel):
    type: ElementType
    id: Annotated[int | None, Field(validate_default=True, frozen=True)] = None

    _subtypes = dict()

    def __init_subclass__(subcls, type=None, **kwargs):
        super().__init_subclass__(**kwargs)
        if type:
            # n.b. if a subclass declares its own _subtypes dict, it'll take precedence over this one.
            # This would allow us to re-use the same type names across different classes.
            if type in subcls._subtypes:
                raise AttributeError(
                    f"Class {subcls} cannot be registered with polymorphic type='{type}' because it's already registered "
                    f" to {subcls._subtypes[type]}"
                )
            subcls._subtypes[type] = subcls

    @field_validator("id")
    def set_id_now(cls, v):
        try:
            id = v or max(ELEMENT_REGISTER) + 1
        except ValueError:
            id = 1
        register(id, ELEMENT_REGISTER)
        return id

    @classmethod
    def _convert_to_real_type(cls, data):
        data_type = data.get("type")

        if data_type is None:
            raise ValueError(f"Missing 'type' for {cls}")

        subcls = cls._subtypes.get(data_type)

        if subcls is None:
            raise TypeError(f"Unsupported sub-type: {data_type}")
        if not issubclass(subcls, cls):
            raise TypeError(f"Inferred class {subcls} is not a subclass of {cls}")

        return subcls(**data)

    @classmethod
    def parse_obj(cls, data):
        return cls._convert_to_real_type(data)
