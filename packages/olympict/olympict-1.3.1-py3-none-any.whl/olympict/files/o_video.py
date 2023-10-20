import os
import shutil
from typing import Optional

from olympict.files.o_file import OlympFile


class OlympVid(OlympFile):
    __id = 0

    def __init__(self, path: Optional[str] = None):
        super().__init__(path)
        if path is None:
            self._tmp_path = f"./{self.__id}.mp4"
            self.__id += 1
        self._tmp_path = ""
        self._fps = 25

    def change_folder_path(self, new_folder_path: str):
        old_path: str = self.path
        self.path = os.path.join(new_folder_path, os.path.basename(self.path))
        shutil.move(old_path, self.path)

    def get_temp_path(self) -> str:
        return self._tmp_path
