import os
from glob import glob
from random import randint
import sys
from typing import (
    Any,
    Callable,
    Dict,
    Generator,
    List,
    Optional,
    Tuple,
    Union,
    cast,
)

import cv2
from natsort import natsorted
import numpy as np


from olympict.files.o_batch import OlympBatch

from olympict.files.o_image import OlympImage
from olympict.files.o_video import OlympVid
from olympict.image_tools import ImTools
from olympict.pipeline import OPipeline
from olympict.types import (
    BBoxAbsolute,
    BBoxRelative,
    Color,
    Img,
    ImgFormat,
    LineAbsolute,
    LineRelative,
    PolygonAbsolute,
    PolygonRelative,
    Size,
)
from olympict.video_saver import PipelineVideoSaver


class ImagePipeline(OPipeline[OlympImage]):
    @staticmethod
    def load_paths(
        paths: List[str],
        metadata_function: Optional[Callable[[str], Any]] = None,
    ) -> "ImagePipeline":
        data = [OlympImage(p) for p in paths]

        if metadata_function is not None:
            for d in data:
                d.metadata = metadata_function(d.path)

        return ImagePipeline(data)

    @staticmethod
    def load_folder(
        path: str,
        extensions: List[str] = ["png", "jpg", "jpeg", "bmp"],
        recursive: bool = False,
        order_func: Optional[Union[bool, Callable[[str], int]]] = True,
        reverse: bool = False,
        metadata_function: Optional[Callable[[str], Any]] = None,
    ) -> "ImagePipeline":
        paths: List[str] = glob(os.path.join(path, "**"), recursive=recursive)

        paths = [p for p in paths if os.path.splitext(p)[1].strip(".") in extensions]

        if order_func is False:
            pass
        elif order_func is True:
            paths = natsorted(paths, reverse=reverse)
        elif order_func is not None:
            paths.sort(key=order_func, reverse=reverse)

        data = [OlympImage(p) for p in paths]

        if metadata_function is not None:
            for d in data:
                d.metadata = metadata_function(d.path)

        return ImagePipeline(data)

    @staticmethod
    def load_folders(
        paths: List[str],
        extensions: List[str] = ["png", "jpg", "jpeg", "bmp"],
        recursive: bool = False,
        order_func: Optional[Union[bool, Callable[[str], int]]] = True,
        reverse: bool = False,
        metadata_function: Optional[Callable[[str], Any]] = None,
    ) -> "ImagePipeline":
        all_data: List[OlympImage] = []
        for path in paths:
            sub_paths: List[str] = glob(os.path.join(path, "**"), recursive=recursive)

            sub_paths = [
                p for p in sub_paths if os.path.splitext(p)[1].strip(".") in extensions
            ]

            if order_func is False:
                pass
            elif order_func is True:
                sub_paths = natsorted(sub_paths, reverse=reverse)
            elif order_func is not None:
                sub_paths.sort(key=order_func, reverse=reverse)

            data = [OlympImage(p) for p in sub_paths]

            if metadata_function is not None:
                for d in data:
                    d.metadata = metadata_function(d.path)

            all_data.extend(data)

        return ImagePipeline(all_data)

    def task(
        self, func: Callable[[OlympImage], OlympImage], count: int = 1
    ) -> "ImagePipeline":
        return ImagePipeline(extending=self.pipeline.task(func, count))

    def task_img(self, func: Callable[[Img], Img], count: int = 1) -> "ImagePipeline":
        def r(o: OlympImage) -> OlympImage:
            o.img = func(o.img)
            return o

        return self.task(r, count)

    def task_path(self, func: Callable[[str], str], count: int = 1) -> "ImagePipeline":
        def r(o: OlympImage) -> OlympImage:
            o.ensure_load()
            o.path = func(o.path)
            return o

        return self.task(r, count)

    def explode(self, explode_function: Callable[[OlympImage], List[OlympImage]]):
        return ImagePipeline(extending=self.pipeline.explode(explode_function))

    def rescale(
        self,
        size: Tuple[float, float],
        pad_color: Optional[Tuple[int, int, int]] = None,
        count: int = 1,
    ) -> "ImagePipeline":
        return self.task(OlympImage.rescale(size, pad_color), count)

    def resize(
        self,
        size: Tuple[int, int],
        pad_color: Optional[Tuple[int, int, int]] = None,
        interpolation: int = cv2.INTER_LINEAR,
        count: int = 1,
    ) -> "ImagePipeline":
        return self.task(OlympImage.resize(size, pad_color, interpolation), count)

    def crop(
        self,
        left: int = 0,
        top: int = 0,
        right: int = 0,
        bottom: int = 0,
        pad_color: Color = (0, 0, 0),
    ) -> "ImagePipeline":
        def r(img: Img) -> Img:
            return ImTools.crop_image(
                img, top=top, left=left, bottom=bottom, right=right, pad_color=pad_color
            )

        return self.task_img(r)

    def random_crop(
        self,
        output_size: Size,
    ) -> "ImagePipeline":
        def r(img: Img) -> Img:
            h, w, _ = img.shape
            t_w, t_h = output_size

            off_x = randint(0, w - t_w - 1)
            off_y = randint(0, h - t_h - 1)

            return img[off_y : off_y + t_h, off_x : off_x + t_w, :]

        return self.task_img(r)

    def filter(self, filter_function: Callable[[OlympImage], bool]) -> "ImagePipeline":
        return ImagePipeline(extending=self.pipeline.filter(filter_function))

    def keep_each_frame_in(
        self, keep_n: int = 1, discard_n: int = 0
    ) -> "ImagePipeline":
        def discarder():
            while True:
                for _ in range(keep_n):
                    yield True
                for _ in range(discard_n):
                    yield False

        d = discarder()

        def get_next(_: Any) -> bool:
            return next(d)

        return ImagePipeline(extending=self.pipeline.filter(get_next))

    def debug_window(self, name: str) -> "ImagePipeline":
        def d(o: "OlympImage") -> "OlympImage":
            cv2.imshow(name, o.img)
            _ = cv2.waitKey(1)
            return o

        return self.task(d)

    def to_video(
        self, img_to_video_path: Callable[[OlympImage], str], fps: int = 25
    ) -> "VideoPipeline":
        return VideoPipeline(
            extending=self.pipeline.class_task(
                PipelineVideoSaver,
                PipelineVideoSaver.process_file,
                [img_to_video_path, fps],
                PipelineVideoSaver.finish,
            )
        )

    def to_format(self, format: ImgFormat) -> "ImagePipeline":
        def change_format(path: str) -> str:
            base, _ = os.path.splitext(path)

            fmt = f".{format}" if "." != format[0] else format

            return base + fmt

        return self.task_path(change_format)

    def save_to_folder(self, folder_path: str) -> "ImagePipeline":
        os.makedirs(folder_path, exist_ok=True)

        def s(o: "OlympImage") -> "OlympImage":
            o.change_folder_path(folder_path)
            o.save()
            return o

        return self.task(s)

    def save(self) -> "ImagePipeline":
        def s(o: "OlympImage") -> "OlympImage":
            o.save()
            return o

        return self.task(s)

    def draw_relative_polygons(
        self,
        polygon_function: Callable[[OlympImage], List[Tuple[PolygonRelative, Color]]],
    ) -> "ImagePipeline":
        def p(o: "OlympImage") -> "OlympImage":
            outputs = polygon_function(o)
            for polygon, color in outputs:
                o.img = ImTools.draw_relative_polygon(o.img, polygon, color)
            return o

        return self.task(p)

    def draw_polygons(
        self,
        polygon_function: Callable[[OlympImage], List[Tuple[PolygonAbsolute, Color]]],
    ) -> "ImagePipeline":
        def p(o: "OlympImage") -> "OlympImage":
            outputs = polygon_function(o)
            for polygon, color in outputs:
                o.img = ImTools.draw_polygon(o.img, polygon, color)
            return o

        return self.task(p)

    def draw_relative_bboxes(
        self,
        bbox_function: Callable[[OlympImage], List[Tuple[BBoxRelative, Color]]],
        font_scale: float = ImTools.font_scale,
    ) -> "ImagePipeline":
        def p(o: "OlympImage") -> "OlympImage":
            outputs = bbox_function(o)
            for polygon, color in outputs:
                o.img = ImTools.draw_relative_bbox(o.img, polygon, color, font_scale)
            return o

        return self.task(p)

    def draw_bboxes(
        self,
        bbox_function: Callable[[OlympImage], List[Tuple[BBoxAbsolute, Color]]],
        font_scale: float = ImTools.font_scale,
    ) -> "ImagePipeline":
        def p(o: "OlympImage") -> "OlympImage":
            for polygon, color in bbox_function(o):
                o.img = ImTools.draw_bbox(o.img, polygon, color, font_scale)
            return o

        return self.task(p)

    def draw_relative_lines(
        self,
        polyline_function: Callable[[OlympImage], List[Tuple[LineRelative, Color]]],
    ) -> "ImagePipeline":
        def p(o: "OlympImage") -> "OlympImage":
            outputs = polyline_function(o)
            for line, color in outputs:
                o.img = ImTools.draw_relative_line(o.img, line, color)
            return o

        return self.task(p)

    def draw_lines(
        self,
        polyline_function: Callable[[OlympImage], List[Tuple[LineAbsolute, Color]]],
    ) -> "ImagePipeline":
        def p(o: "OlympImage") -> "OlympImage":
            outputs = polyline_function(o)
            for line, color in outputs:
                o.img = ImTools.draw_line(o.img, line, color)
            return o

        return self.task(p)

    def draw_heatmap(
        self, heatmap_function: Callable[[OlympImage], Img]
    ) -> "ImagePipeline":
        def p(o: "OlympImage") -> "OlympImage":
            outputs = heatmap_function(o)
            o.img = ImTools.draw_heatmap(o.img, outputs)
            return o

        return self.task(p)

    def draw_segmentation_maps(
        self, segmentation_map: Callable[[OlympImage], Img], color: Color
    ) -> "ImagePipeline":
        def p(o: "OlympImage") -> "OlympImage":
            seg_map = segmentation_map(o)
            o.img = ImTools.draw_segmentation_map(o.img, seg_map, color)
            return o

        return self.task(p)

    def class_task_img(
        self,
        class_constructor: Any,
        store_results_in_metadata_key: str,
        class_method: Callable[[Any, Img], Any],
        close_method: Optional[Callable[[Any], Any]] = None,
        class_args: List[Any] = [],
        class_kwargs: Dict[str, Any] = {},
    ):
        """_summary_

        Args:
            class_constructor (Any): _description_
            class_method (Callable[[Img], Any]): _description_
            store_results_in_metadata_key (str): _description_
            class_args (List[Any], optional): _description_. Defaults to [].
            close_method (Optional[Callable[[OlympImage], Any]], optional): _description_. Defaults to None.
            class_kwargs (Dict[str, Any], optional): _description_. Defaults to {}.

        Returns:
            _type_: _description_
        """

        class HigherOrderClass(class_constructor):  # type: ignore
            def process_override_function(self, o: OlympImage):
                method = self.__getattribute__(class_method.__name__)
                o.metadata[store_results_in_metadata_key] = method(np.copy(o.img))
                return o

        return self.class_task(
            HigherOrderClass,
            HigherOrderClass.process_override_function,
            close_method,
            class_args,
            class_kwargs,
        )

    def class_task(
        self,
        class_constructor: Any,
        class_method: Callable[[Any, OlympImage], OlympImage],
        close_method: Optional[Callable[[Any], Any]] = None,
        class_args: List[Any] = [],
        class_kwargs: Dict[str, Any] = {},
    ) -> "ImagePipeline":
        """This operation enables the use of a stateful processing using a class

        Args:
            class_constructor (Any): the class constructor, ex: MyClass
            class_method (Callable[[Any, OlympImage], OlympImage]): The processing method applied to each packet, ex: MyClass.process_img
            close_method (Optional[Callable[[Any], Any]], optional): If provided, the method used when the pipeline has processed all packets . Defaults to None.
            class_args (List[Any], optional): The constructor args. Defaults to [].
            class_kwargs (Dict[str, Any], optional): The constructor Kwargs. Defaults to {}.

        Raises:
            Exception: Error if the pipeline is not well defined

        Returns:
            ImagePipeline: the output ImagePipeline
        """

        return ImagePipeline(
            extending=self.pipeline.class_task(
                class_constructor, class_method, class_args, close_method, class_kwargs
            )
        )

    def batch(self, batch_size: int) -> "BatchPipeline":
        return BatchPipeline(
            extending=self.pipeline.batch(batch_size).task(OlympBatch.from_images)
        )

    def classify(
        self,
        huggingface_id: str,
        revision: Optional[str] = None,
        huggingface_token: Optional[str] = None,
    ) -> "ImagePipeline":
        from olympict.hf_class import HuggingFaceModel

        try:
            return self.class_task(
                HuggingFaceModel,
                HuggingFaceModel.infer,
                class_args=(huggingface_id, revision, huggingface_token),
            )
        except Exception as e:
            print("Could not initialize model", huggingface_id, "\n", e)
            sys.exit(1)


class BatchPipeline(OPipeline[OlympBatch]):
    def task(
        self, func: Callable[[OlympBatch], OlympBatch], count: int = 1
    ) -> "BatchPipeline":
        return BatchPipeline(extending=self.pipeline.task(func, count))

    def task_img_batch(
        self, func: Callable[[Img], Img], count: int = 1
    ) -> "BatchPipeline":
        def r(o: OlympBatch) -> OlympBatch:
            o.data = func(o.data)
            return o

        return self.task(r, count)

    def to_images(self) -> "ImagePipeline":
        return ImagePipeline(extending=self.pipeline.explode(OlympBatch.to_images))

    def class_task(
        self,
        class_constructor: Any,
        class_method: Callable[[Any, OlympBatch], OlympBatch],
        close_method: Optional[Callable[[Any], Any]] = None,
        class_args: List[Any] = [],
        class_kwargs: Dict[str, Any] = {},
    ) -> "BatchPipeline":
        """This operation enables the use of a stateful processing using a class

        Args:
            class_constructor (Any): the class constructor, ex: MyClass
            class_method (Callable[[Any, OlympBatch], OlympBatch]): The processing method applied to each packet, ex: MyClass.process_img
            close_method (Optional[Callable[[Any], Any]], optional): If provided, the method used when the pipeline has processed all packets . Defaults to None.
            class_args (List[Any], optional): The constructor args. Defaults to [].
            class_kwargs (Dict[str, Any], optional): The constructor Kwargs. Defaults to {}.

        Raises:
            Exception: Error if the pipeline is not well defined

        Returns:
            BatchPipeline: the output BatchPipeline
        """
        return BatchPipeline(
            extending=self.pipeline.class_task(
                class_constructor, class_method, class_args, close_method, class_kwargs
            )
        )

    def class_task_batch(
        self,
        class_constructor: Any,
        store_results_in_metadata_key: str,
        class_method: Callable[[Any, Img], Any],
        close_method: Optional[Callable[[Any], Any]] = None,
        class_args: List[Any] = [],
        class_kwargs: Dict[str, Any] = {},
    ) -> "BatchPipeline":
        """
        Args:
            class_constructor (Any): _description_
            class_method (Callable[[Img], Any]): _description_
            store_results_in_metadata_key (str): _description_
            class_args (List[Any], optional): _description_. Defaults to [].
            close_method (Optional[Callable[[OlympImage], Any]], optional): _description_. Defaults to None.
            class_kwargs (Dict[str, Any], optional): _description_. Defaults to {}.
        """

        class HigherOrderClass(class_constructor):  # type: ignore
            def process_override_function(self, o: OlympBatch):
                method = self.__getattribute__(class_method.__name__)
                res = method(np.copy(o.data))
                for i in range(res.shape[0]):
                    o.metadata[i][store_results_in_metadata_key] = res[i]
                return o

        return self.class_task(
            HigherOrderClass,
            HigherOrderClass.process_override_function,
            close_method,
            class_args,
            class_kwargs,
        )


class VideoPipeline(OPipeline[OlympVid]):
    @staticmethod
    def load_folder(
        path: str,
        extensions: List[str] = ["mkv", "mp4"],
        recursive: bool = False,
        order_func: Optional[Union[bool, Callable[[str], int]]] = True,
        reverse: bool = False,
    ) -> "VideoPipeline":
        paths: List[str] = glob(os.path.join(path, "**"), recursive=recursive)
        paths = [p for p in paths if os.path.splitext(p)[1].strip(".") in extensions]

        if order_func is False:
            pass
        elif order_func is True:
            paths = natsorted(paths, reverse=reverse)
        elif order_func is not None:
            paths.sort(key=order_func, reverse=reverse)

        data = [OlympVid(p) for p in paths]

        return VideoPipeline(data)

    def task(
        self, func: Callable[[OlympVid], OlympVid], count: int = 1
    ) -> "VideoPipeline":
        return VideoPipeline(extending=self.pipeline.task(func, count))

    def move_to_folder(self, folder_path: str) -> "VideoPipeline":
        os.makedirs(folder_path, exist_ok=True)

        def s(o: "OlympVid") -> "OlympVid":
            o.change_folder_path(folder_path)
            return o

        return self.task(s)

    def to_sequence(self) -> "ImagePipeline":
        def generator(o: "OlympVid") -> Generator[OlympImage, None, None]:
            capture: Any = cv2.VideoCapture(o.path)
            res, frame = cast(Tuple[bool, Img], capture.read())
            idx = 0
            while res:
                new_path = f"{o.path}_{idx}.png"
                yield OlympImage.from_buffer(
                    frame, new_path, {"video_path": o.path, "video_frame": idx}
                )
                res, frame = cast(Tuple[bool, Img], capture.read())
                idx += 1
            capture.release()
            return

        return ImagePipeline(extending=self.pipeline.explode(generator))
