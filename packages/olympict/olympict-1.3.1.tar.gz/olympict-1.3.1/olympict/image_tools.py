from typing import List

import cv2  # type: ignore
import numpy as np

from olympict.types import (
    BBoxAbsolute,
    BBoxRelative,
    Color,
    Img,
    LineAbsolute,
    LineRelative,
    PointAbsolute,
    PointRelative,
    PolygonAbsolute,
    PolygonRelative,
    Size,
)


class ImTools:
    font = 0
    font_scale = 0.4
    blue: Color = (255, 0, 0)
    green: Color = (0, 255, 0)
    red: Color = (0, 0, 255)
    black: Color = (0, 0, 0)
    grey: Color = (127, 127, 127)
    white: Color = (255, 255, 255)

    @staticmethod
    def load(path: str) -> Img:
        return cv2.imread(path)

    @staticmethod
    def load_multiple(paths: List[str]) -> List[Img]:
        return [ImTools.load(path) for path in paths]

    @staticmethod
    def pad_square(image: Img, color: Color = (0, 0, 0)) -> Img:
        """
        Pads an image to fit in a square
        Args:
            image (Image): cv2.Image
        Returns:
            Image: cv2.Image
        """
        max_dim = max(image.shape[:-1])
        padded_image = ImTools.pad_to_output_size(image, (max_dim, max_dim), color)
        return padded_image

    @staticmethod
    def pad_to_ratio(image: Img, ratio: float, color: Color = (0, 0, 0)) -> Img:
        """
        Pads an image to the specified ratio

        Args:
            image (Image): cv2.Image
            ratio (float): width / height

        Returns:
            Image: cv2.Image
        """
        height, width = image.shape[:-1]
        image_ratio = width / height
        if image_ratio < ratio:
            # keep height
            dims = (height, int(round(height * ratio)))
        else:
            # keep width
            dims = (int(round(width / ratio)), width)

        return ImTools.pad_to_output_size(image, dims, color)

    @staticmethod
    def pad_to_output_size(
        image: Img,
        size: Size,
        color: Color = (0, 0, 0),
        interpolation: int = cv2.INTER_LINEAR,
    ) -> Img:
        """Pads an image to the specified size (adds black pixels)

        Args:
            image (Image): cv2.Image
            size (Size): height, width

        Returns:
            Image: cv2.Image
        """
        height, width = image.shape[:-1]

        out_h, out_w = size

        desired_ratio = out_w / out_h
        input_ratio = width / height

        if input_ratio > desired_ratio:
            resized = cv2.resize(
                image, (out_w, int(out_w / input_ratio)), interpolation=interpolation
            )
        else:
            resized = cv2.resize(
                image, (int(out_h * input_ratio), out_h), interpolation=interpolation
            )

        resized_h, resized_w, _ = resized.shape

        pad_top = int((out_h - resized_h) / 2)
        pad_left = int((out_w - resized_w) / 2)
        pad_bottom = int(out_h - pad_top - resized_h)
        pad_right = int(out_w - pad_left - resized_w)

        padded_image = cv2.copyMakeBorder(
            resized,
            pad_top,
            pad_bottom,
            pad_left,
            pad_right,
            cv2.BORDER_CONSTANT,
            value=color,
        )

        return padded_image

    @staticmethod
    def crop_image(
        image: Img,
        left: int = 0,
        top: int = 0,
        right: int = 0,
        bottom: int = 0,
        pad_color: Color = (0, 0, 0),
    ) -> Img:
        """Crops an image. It can also pad an image if numbers are < 0

        Args:
            image (Image): Input cv2 image
            top (int, optional): pixels to remvoe from the top. Defaults to 0.
            left (int, optional): pixels to remvoe from the left. Defaults to 0.
            bottom (int, optional): pixels to remvoe from the bottom. Defaults to 0.
            right (int, optional): pixels to remvoe from the right. Defaults to 0.
            pad_color (Color, optional): Color to use if padding.

        Returns:
            Image: The cv2 image cropped
        """

        h, w, channels = image.shape

        new_h = h - top - bottom
        new_w = w - left - right

        img = np.ones((new_h, new_w, channels), dtype=np.uint8) * pad_color

        left_source = max(left, 0)
        left_destination = max(-left, 0)

        top_source = max(top, 0)
        top_destination = max(-top, 0)

        copy_w = w - max(left, 0) - max(right, 0)
        copy_h = h - max(top, 0) - max(bottom, 0)

        img[
            top_destination : top_destination + copy_h,
            left_destination : left_destination + copy_w,
            :,
        ] = image[
            top_source : top_source + copy_h,
            left_source : left_source + copy_w,
            :,
        ]

        return img

    @staticmethod
    def draw_heatmap(image: Img, map: Img, alpha_map: float = 0.5) -> Img:
        """
        Args:
            image (Image): cv2.image (HWC)
            map (Image): [0-255] cv2.image (HW)
            alpha_map (float): [0-1] balance between image and map
        """

        heatmap_img = cv2.applyColorMap(np.array(map, dtype=np.uint8), cv2.COLORMAP_JET)

        heatmap_img = cv2.resize(
            heatmap_img, image.shape[:2][::-1], interpolation=cv2.INTER_LINEAR
        )

        output = cv2.addWeighted(
            heatmap_img,
            alpha_map,
            image,
            1 - alpha_map,
            0,
            dtype=cv2.PARAM_UNSIGNED_INT,
        )

        return output

    @staticmethod
    def draw_segmentation_map(image: Img, map: Img, color: Color) -> Img:
        """
        Args:
            image (Image): cv2.image (HWC)
            map (Image): [0/1] bool cv2.image (HW)
            color (Color)
        """

        output = image.copy()

        output[map] = color

        return output

    @staticmethod
    def draw_multiple_heatmaps(image: Img, maps: Img, alpha_map: float = 0.5) -> Img:
        """
        Args:
            image (Image): cv2.image (HWC)
            map (Image): [0-255] cv2.image (HW)
            alpha_map (float): [0-1] balance between image and map
        """
        max_map: Img = np.max(maps, axis=-1)
        return ImTools.draw_heatmap(image, max_map, alpha_map=alpha_map)

    @staticmethod
    def convert_point_relative_to_absolute(
        object: PointRelative, w: int, h: int
    ) -> PointAbsolute:
        x, y = object
        return (int(round(x * w)), int(round(y * h)))

    @staticmethod
    def convert_point_absolute_to_relative(
        object: PointAbsolute, w: int, h: int
    ) -> PointRelative:
        x, y = object
        return (float(x) / w, float(y) / h)

    @staticmethod
    def convert_bbox_relative_to_absolute(
        object: BBoxRelative, w: int, h: int
    ) -> BBoxAbsolute:
        x1, y1, x2, y2, class_name, confidence = object
        return (
            *ImTools.convert_point_relative_to_absolute((x1, y1), w, h),
            *ImTools.convert_point_relative_to_absolute((x2, y2), w, h),
            class_name,
            confidence,
        )

    @staticmethod
    def convert_bbox_absolute_to_relative(
        object: BBoxAbsolute, w: int, h: int
    ) -> BBoxRelative:
        x1, y1, x2, y2, class_name, confidence = object
        return (
            *ImTools.convert_point_absolute_to_relative((x1, y1), w, h),
            *ImTools.convert_point_absolute_to_relative((x2, y2), w, h),
            class_name,
            confidence,
        )

    @staticmethod
    def draw_line(image: Img, line: LineAbsolute, color: Color, size: float = 1) -> Img:
        for i in range(len(line) - 1):
            from_point = line[i]
            to_point = line[i + 1]
            image = cv2.line(image, from_point, to_point, color, thickness=size)
        return image

    @staticmethod
    def draw_relative_line(
        image: Img, line: LineRelative, color: Color, size: float = 1
    ) -> Img:
        h, w, _ = image.shape

        abs_line = [ImTools.convert_point_relative_to_absolute(p, w, h) for p in line]

        return ImTools.draw_line(image, abs_line, color, size)

    @staticmethod
    def draw_bbox(
        image: Img, bbox: BBoxAbsolute, color: Color, font_scale: float
    ) -> Img:
        x1, y1, x2, y2, class_name, conf = bbox
        image = cv2.rectangle(image, (x1, y1), (x2, y2), color=color, thickness=1)

        image = cv2.putText(
            image,
            class_name if conf is None else f"{class_name}: {conf:0.2f}%",
            (x1 + int(1 + 0.3 * font_scale), y1 + int(20 * font_scale)),
            ImTools.font,
            font_scale,
            color,
            1,
            cv2.LINE_AA,
        )
        return image

    @staticmethod
    def draw_relative_bbox(
        image: Img, bbox: BBoxRelative, color: Color, font_scale: float
    ) -> Img:
        h, w, _ = image.shape

        abs_bbox = ImTools.convert_bbox_relative_to_absolute(bbox, w, h)

        return ImTools.draw_bbox(image, abs_bbox, color, font_scale)

    @staticmethod
    def draw_polygon(image: Img, polygon: PolygonAbsolute, color: Color) -> Img:
        image = cv2.polylines(image, [np.array(polygon)], True, color, thickness=1)

        return image

    @staticmethod
    def draw_relative_polygon(
        image: Img, polygon: PolygonRelative, color: Color
    ) -> Img:
        h, w, _ = image.shape

        abs_polygon = [
            ImTools.convert_point_relative_to_absolute(p, w, h) for p in polygon
        ]

        return ImTools.draw_polygon(image, abs_polygon, color)
