from pydantic import model_validator, Field, field_validator
from typing import Union

from .base import PolymorphicBaseElement, ElementType
from .nodes import Node
from ..base import Base


NUM_ELEMENT_NODES = {
    ElementType.tube: 2,
    ElementType.conicaltube: 2,
    ElementType.cuboid: 2,
    ElementType.cone: 2,
}


class Element(PolymorphicBaseElement):
    nodes: list[Node]

    @model_validator(mode="after")
    def check_number_of_nodes(self):
        if len(self.nodes) != NUM_ELEMENT_NODES[self.type]:
            raise ValueError(
                f"Element of type {self.type} should have {NUM_ELEMENT_NODES[self.type]} nodes, not {len(self.nodes)}"
            )
        return self


class Tube(Element):
    type: ElementType = Field(default=ElementType.tube, frozen=True)
    diameter: float
    thickness: float


class ConicalTube(Element):
    type: ElementType = Field(default=ElementType.conicaltube, frozen=True)
    diameters: list[float]
    thicknesses: list[float]

    @field_validator("diameters")
    def set_diameters_now(cls, diameters):
        if len(diameters) != 2:
            raise ValueError(
                f"Conical sections must have 2 diameters, not {len(diameters)} "
            )
        return diameters

    @field_validator("thicknesses")
    def set_thicknesses_now(cls, thicknesses):
        if len(thicknesses) != 2:
            raise ValueError(
                f"Conical sections must have 2 thicknesses, not {len(thicknesses)} "
            )
        return thicknesses


class Cuboid(Element):
    type: ElementType = Field(default=ElementType.cuboid, frozen=True)
    width: float
    height: float


class Cone(Element):
    type: ElementType = Field(default=ElementType.cone, frozen=True)
    diameter: float


ELEMENT_BUILDER = {
    ElementType.tube: Tube,
    ElementType.conicaltube: ConicalTube,
    ElementType.cuboid: Cuboid,
    ElementType.cone: Cone,
}


class ElementSet(Base):
    elements: list[Union[Cone, ConicalTube, Cuboid, Tube]]

    # Access data before to handle different types of Element
    @field_validator("elements", mode="before")
    def select_element_type(cls, values):
        elements = []
        for el in values:
            if isinstance(el, Element):
                elements.append(el)
            else:
                # Loading from dict
                eltype = el.get("type")
                elements.append(ELEMENT_BUILDER[ElementType[eltype]](**el))
        return elements
