import os
from typing import Callable, Optional

import cv2  # type: ignore
import numpy as np

from olympict.files.o_image import OlympImage


class VideoSaver:
    def __init__(self, output_name: str, fps: int = 30):
        self.writer: cv2.writer
        self.empty: bool = True
        self.fps = fps
        self.output_path = output_name

    def new_writer(self, w: int, h: int):
        self.writer = cv2.VideoWriter(
            self.output_path, cv2.VideoWriter_fourcc(*"mp4v"), self.fps, (w, h)
        )
        self.empty = False

    def add_frame(self, frame: cv2.Mat):
        if self.empty:
            self.new_writer(*frame.shape[:2][::-1])
        self.writer.write(frame.astype(np.uint8))

    def finish(self):
        self.writer.release()


class PipelineVideoSaver:
    def __init__(
        self, img_to_path_function: Callable[[OlympImage], str], fps: int = 25
    ):
        self.vs: Optional[VideoSaver] = None
        self.fps = fps
        self.img_to_path_function = img_to_path_function

    def _ensure_folder(self, path: str):
        folder = os.path.dirname(path)
        os.makedirs(folder, exist_ok=True)

    def process_file(self, file: OlympImage):
        path = self.img_to_path_function(file)
        self._ensure_folder(path)
        if self.vs is None:
            self.vs = VideoSaver(path, self.fps)
            self.vs.add_frame(file.img)
        elif self.vs.output_path == path:
            self.vs.add_frame(file.img)
        else:
            self.vs.finish()
            self.vs = VideoSaver(path, self.fps)
            self.vs.add_frame(file.img)

    def finish(self):
        if self.vs is not None:
            self.vs.finish()
