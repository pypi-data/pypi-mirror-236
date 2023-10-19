from pydantic import BaseModel, field_validator, Field
import uuid
from typing_extensions import Annotated


class Base(BaseModel):
    name: str
    id: Annotated[str | None, Field(validate_default=True, frozen=True)] = None

    @field_validator("id")
    @classmethod
    def set_id_now(cls, v):
        return v or str(uuid.uuid4())
