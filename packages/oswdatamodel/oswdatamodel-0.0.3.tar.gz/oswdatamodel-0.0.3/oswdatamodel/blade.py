from pydantic import field_validator
from pathlib import Path

from .base import Base
from .geometry.vectors import Vector3

SUPPORTED_MODELS = [".gltf", ".glb"]


class Blade(Base):
    url: str  # url to the gltf or glb file to load
    scale: Vector3

    @field_validator("url")
    def set_url_now(cls, url):
        url_path = Path(url)
        if url_path.suffix.lower() not in SUPPORTED_MODELS:
            raise TypeError(
                f"Cannot support blade model of file type {url_path.suffix}, please provide one of {SUPPORTED_MODELS}"
            )
        return url
