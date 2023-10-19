from typing import Optional

from olympict.types import Size


class OlympFile:
    def __init__(self, path: Optional[str] = None):
        self.path = path or ""

    @property
    def size(self) -> Size:
        raise NotImplementedError("No size for this object")
