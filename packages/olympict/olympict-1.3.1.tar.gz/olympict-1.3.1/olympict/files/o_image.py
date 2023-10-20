import os
import shutil
from typing import Any, Callable, Dict, Optional, Tuple

import cv2  # type: ignore
import numpy as np

from olympict.files.o_file import OlympFile
from olympict.image_tools import ImTools
from olympict.types import Color, Img, Size


class OlympImage(OlympFile):
    __id = 0

    def __init__(self, path: Optional[str] = None):
        super().__init__(path)
        self._img: Optional[Img] = None
        if path is None:
            self.path = f"./{self.__id}.png"
            self.__id += 1
            self._img = np.zeros((1, 1, 3), dtype=np.uint8)
        self.metadata: Dict[str, Any] = {}

    @property
    def img(self) -> Img:
        self.ensure_load()
        return self._img

    @img.setter
    def img(self, image: Img):
        self._img = image

    def ensure_load(self):
        if self._img is None:
            self._img = cv2.imread(self.path)

    @staticmethod
    def resize(
        size: Size,
        pad_color: Optional[Color] = None,
        interpolation: int = cv2.INTER_LINEAR,
    ) -> Callable[["OlympImage"], "OlympImage"]:
        def r(o: "OlympImage") -> "OlympImage":
            if pad_color is None:
                o.img = cv2.resize(o.img, size, interpolation=interpolation)
            else:
                o.img = ImTools.pad_to_output_size(
                    o.img, size, pad_color, interpolation=interpolation
                )
            return o

        return r

    @staticmethod
    def rescale(
        scales: Tuple[float, float],
        pad_color: Optional[Color] = None,
        interpolation: int = cv2.INTER_LINEAR,
    ) -> Callable[["OlympImage"], "OlympImage"]:
        """Rescale function
        This function applies a scale [x_s, y_s] to a given image
        The resulting image dimensions are [w * x_s, h * y_s]
        """

        def r(o: "OlympImage") -> "OlympImage":
            w, h = o.size
            x_scale, y_scale = scales
            size = (int(round(w * x_scale)), int(round(h * y_scale)))
            if pad_color is None:
                o.img = cv2.resize(o.img, size, interpolation=interpolation)
            else:
                o.img = ImTools.pad_to_output_size(
                    o.img, size, pad_color, interpolation=interpolation
                )
            return o

        return r

    def move_to_path(self, path: str):
        """This function moves images to a new location. If path is a directory, then it will keep its old name and move to the new directory.
        Else it will be given path as a new name (This might be bad for multiple images).
        """
        #  TODO: Ensure folder or not
        if os.path.isdir(path):
            _, filename = os.path.split(self.path)
            path = os.path.join(path, filename)
        shutil.move(self.path, path)
        self.path = os.path.abspath(path)

    def change_folder_path(self, new_folder_path: str):
        self.ensure_load()
        self.path = os.path.join(new_folder_path, os.path.basename(self.path))

    def move_to(self, func: Callable[[str], str]):
        self.ensure_load()
        output = func(self.path)
        self.move_to_path(output)

    def save(self):
        self.ensure_load()
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        _ = cv2.imwrite(self.path, self.img)

    def save_as(self, path: str):
        self.ensure_load()
        if os.path.isdir(path):
            _, filename = os.path.split(self.path)
            path = os.path.join(path, filename)

        self.path = os.path.abspath(path)
        self.save()

    @property
    def size(self) -> Size:
        h, w, _ = self.img.shape
        return (w, h)

    @staticmethod
    def load(path: str, metadata: Dict[str, Any] = {}) -> "OlympImage":
        o = OlympImage()
        o.path = path
        o.img = cv2.imread(o.path)
        o.metadata = metadata
        return o

    @staticmethod
    def from_buffer(
        buffer: Img, path: str = "", metadata: Dict[str, Any] = {}
    ) -> "OlympImage":
        o = OlympImage()
        o.path = path
        o.img = buffer
        o.metadata = metadata
        return o
