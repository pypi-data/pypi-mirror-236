from typing import Callable, Generator, Tuple

from olympict.types import Img, Size


class ObjPipeline:
    def resize(self, size: Size, count: int = 1):
        """
        Args:
            size (Size): width, height
        """

    def from_generator(self, generator: Generator[Img, None, None]) -> "ObjPipeline":
        raise NotImplementedError()

    def rescale(self, size: Tuple[float, float], count: int = 1) -> "ObjPipeline":
        """
        Args:
            size (Tuple[float, float]): width multiplier, height multiplier
        """
        raise NotImplementedError()

    def crop(self, size: Size, count: int = 1) -> "ObjPipeline":
        """
        Args:
            size (Size): width, height
        """
        raise NotImplementedError()

    def img_task(self, img_func: Callable[[Img], Img]) -> "ObjPipeline":
        raise NotImplementedError()

    def path_task(self, path_func: Callable[[str], str]) -> "ObjPipeline":
        raise NotImplementedError()
