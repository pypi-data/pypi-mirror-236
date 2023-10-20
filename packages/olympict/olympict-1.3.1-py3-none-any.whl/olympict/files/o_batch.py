from typing import Any, Dict, List

import numpy as np

from olympict.files.o_file import OlympFile
from olympict.files.o_image import OlympImage
from olympict.types import Img, Size


class OlympBatch(OlympFile):
    def __init__(
        self, data: Img, paths: List[str] = [], metadata: List[Dict[str, Any]] = []
    ):
        assert len(data.shape) >= 4
        self.data = data
        self.paths = paths
        self.metadata = metadata

    @property
    def size(self) -> Size:
        _, h, w, _ = self.data.shape
        return (w, h)

    @staticmethod
    def from_images(images: List[OlympImage]) -> "OlympBatch":
        data = np.array([i.img for i in images])
        paths = [i.path for i in images]
        metadata = [i.metadata for i in images]

        return OlympBatch(
            data,
            paths,
            metadata,
        )

    @staticmethod
    def to_images(batch: "OlympBatch") -> List[OlympImage]:
        out = [
            OlympImage.from_buffer(
                batch.data[i, :, :, :], batch.paths[i], batch.metadata[i]
            )
            for i in range(batch.data.shape[0])
        ]
        return out
