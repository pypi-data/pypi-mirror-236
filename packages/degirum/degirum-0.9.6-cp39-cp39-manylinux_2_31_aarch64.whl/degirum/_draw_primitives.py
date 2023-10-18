#
# _draw_primitives.py - DeGirum Python SDK: draw primitives for result postprocessing
# Copyright DeGirum Corp. 2022
#
# Implements draw primitive classes to handle different types of image manipulations
#

import pdb
import importlib
import importlib.util
from pathlib import Path
from typing import overload

import numpy

from .exceptions import DegirumException


def _luminance(color: tuple) -> float:
    """Calculate luminance from RGB color"""
    return 0.2126 * color[0] + 0.7152 * color[1] + 0.0722 * color[2]


def _inv_conversion_calc(conversion, width, height):
    """Invert conversion function calculation

    - `conversion`: conversion function to invert
    - `width`: max conversion width
    - `height`: max conversion height
    """
    p1 = (width / 2, height / 2)
    p2 = (width / 2 - 1, height / 2 - 1)
    f1 = conversion(*p1)
    f2 = conversion(*p2)
    a = ((f2[0] - f1[0]) / (p2[0] - p1[0]), (f2[1] - f1[1]) / (p2[1] - p1[1]))
    b = (f1[0] - p1[0] * a[0], f1[1] - p1[1] * a[1])
    return lambda x, y: ((x - b[0]) / a[0], (y - b[1]) / a[1])


def _image_segmentation_overlay(
    conversion, overlay_data, original_width, original_height, lut
):
    """Return input image scaled with respect to the provided image transformation callback with overlay data added

    - `conversion`: coordinate conversion function accepting two arguments (x,y) and returning two-element tuple
    - `overlay_data`: overlay data to blend on top of input image
    - `original_width`: original image width
    - `original_height`: original image height
    - `lut`: overlay data look up table in RGB format
    """
    assert isinstance(overlay_data, numpy.ndarray)
    import cv2
    from PIL import Image

    # map corners from original image to model output
    height, width = overlay_data.shape
    inv_conversion = _inv_conversion_calc(conversion, width, height)
    p1 = [int(i) for i in inv_conversion(0, 0)]
    p2 = [int(i) for i in inv_conversion(original_width, original_height)]

    img = overlay_data[
        max(p1[1], 0) : min(p2[1], width), max(p1[0], 0) : min(p2[0], height)
    ]

    # add padding to cropped image
    if p1[0] < 0 or p1[1] < 0 or p2[0] > width or p2[1] > height:
        background = numpy.zeros((p2[1] - p1[1], p2[0] - p1[0]), img.dtype)
        background[
            abs(p1[1]) : (abs(p1[1]) + img.shape[0]),
            abs(p1[0]) : (abs(p1[0]) + img.shape[1]),
        ] = img
        img = background

    pil_img = Image.fromarray(img)
    pil_img = pil_img.resize(
        (original_width, original_height), Image.Resampling.NEAREST
    )
    img = numpy.array(pil_img)
    lut = cv2.cvtColor(lut, cv2.COLOR_RGB2BGR)
    return cv2.LUT(cv2.merge((img, img, img)), lut)


def _create_alpha_channel(img, alpha):
    """Convert BGR to RGBA image where all non-black pixels has specified alpha channel value, and zero otherwise

    -`img`: image to convert
    -`alpha`: alpha channel value to set for non-black pixels
    """
    import cv2

    mask = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) != 0
    res = numpy.concatenate(
        (img, numpy.zeros((*mask.shape, 1), dtype=numpy.uint8)), axis=-1
    )
    res[mask] = res[mask] + [0, 0, 0, alpha]
    return cv2.cvtColor(res, cv2.COLOR_BGRA2RGBA)


class _PrimitivesDrawPIL:
    """Drawing class for PIL backend"""

    def __init__(self, image, alpha, font_scale):
        """Constructor.

        - image: native image object
        - alpha: alpha-blend weight for overlay details
        - font_scale: font scale to use for overlay details
        """

        self._pil = importlib.import_module("PIL.Image")
        self._draw = importlib.import_module("PIL.ImageDraw")
        self._font = importlib.import_module("PIL.ImageFont")
        self._original_image = image
        self._image = self._pil.new("RGBA", image.size)
        self._alpha = alpha
        self._font_to_draw = self._font.truetype(
            str(Path(__file__).parent.resolve() / "LiberationMono-Regular.ttf"),
            size=int(font_scale * 12),
        )

    def _adj_color(self, color):
        return color + (int(255 * self._alpha),)

    def draw_circle(self, cx, cy, radius, width, color, fill=False):
        """Draw circle.

        - cx: X coordinate of center
        - cy: Y coordinate of center
        - radius: circle radius
        - width: line width
        - color: color to use
        - fill: whether to fill the circle
        """
        draw = self._draw.Draw(self._image)
        draw.ellipse(
            [cx - radius, cy - radius, cx + radius, cy + radius],
            outline=self._adj_color(color),
            width=width,
            fill=self._adj_color(color) if fill else None,
        )

    def text_size(self, text):
        """Calculate text box width, height, and baseline (y-coordinate of the baseline relative to the bottom-most text point).

        - text: text to calculate box size

        Returns tuple containing text width, text height, and baseline
        """
        ascent, descent = self._font_to_draw.getmetrics()
        bbox = self._font_to_draw.getbbox(text)
        text_w = abs(bbox[2] - bbox[0])
        text_h = abs(bbox[3] - bbox[1]) + descent
        return text_w, text_h, 0

    def draw_text(self, px, py, color, text) -> tuple:
        """Draw text string.

        - px: X coordinate of upper left point
        - py: Y coordinate of upper left point
        - color: color to use
        - text: text to draw

        Returns drawn text label bounding box coordinates
        """
        draw = self._draw.Draw(self._image)
        draw.text((px, py), text, font=self._font_to_draw, fill=self._adj_color(color))
        text_w, text_h, _ = self.text_size(text)
        return (px, py, px + text_w, py + text_h)

    def draw_text_label(self, x1, y1, x2, y2, color, text, line_width) -> tuple:
        """Draw text label near given rectangular frame so it will be always visible

        - x1: X coordinate of left lower point of frame
        - y1: Y coordinate of left lower point of frame
        - x2: X coordinate of upper right point of frame
        - y2: Y coordinate of upper right point of frame
        - color: color to use
        - text: text to draw

        Returns drawn text label bounding box coordinates
        """

        draw = self._draw.Draw(self._image)

        margin = 2
        text_w, text_h, _ = self.text_size(text)
        bbox_w = text_w + 2 * margin
        bbox_h = text_h + 2 * margin

        if y1 >= bbox_h:
            ty = y1 - bbox_h + margin + line_width - 1  # above frame top
        elif y2 + bbox_h < self._image.size[1]:
            ty = y2 + margin - line_width + 1  # below frame bottom
        else:
            ty = y1 + margin  # below frame top

        if x1 + bbox_w < self._image.size[0]:
            tx = x1 + margin  # from frame left
        elif x2 >= bbox_w:
            tx = x2 - bbox_w + margin
        elif self._image.size[0] >= bbox_w:
            tx = self._image.size[0] - bbox_w + margin  # to image right
        else:
            tx = margin  # from image left

        bbox = (tx - margin, ty - margin, tx + text_w + margin, ty + text_h + margin)
        draw.rectangle(
            bbox,
            fill=self._adj_color(color),
            outline=self._adj_color(color),
            width=1,
        )

        text_color = (0, 0, 0) if _luminance(color) > 180 else (255, 255, 255)
        self.draw_text(tx, ty, text_color, text)
        return bbox

    def draw_line(self, x1, y1, x2, y2, width, color):
        """Draw line.

        - x1: X coordinate of beginning point
        - y1: Y coordinate of beginning point
        - x2: X coordinate of ending point
        - y2: Y coordinate of ending point
        - width: line width
        - color: color to use
        """
        draw = self._draw.Draw(self._image)
        draw.line([x1, y1, x2, y2], fill=self._adj_color(color), width=width)

    def draw_box(self, x1, y1, x2, y2, width, color):
        """Draw rectangle.

        - x1: X coordinate of left lower point
        - y1: Y coordinate of left lower point
        - x2: X coordinate of upper right point
        - y2: Y coordinate of upper right point
        - width: line width
        - color: color to use
        """
        draw = self._draw.Draw(self._image)
        draw.rectangle([x1, y1, x2, y2], outline=self._adj_color(color), width=width)

    def image_overlay(self):
        """Return image overlay with proper blending"""
        return self._pil.composite(
            self._image, self._original_image, self._image.getchannel(3)
        )

    def image_overlay_extend(self, width, height, fill_color):
        """Update input image by extending its size.

        - width: width to extend up to
        - height: height value to extend
        - fill_color: color to use use if any form of padding is used

        Returns original image width and height
        """
        original_w = self._original_image.width
        original_h = self._original_image.height
        w = max(self._original_image.width, width)
        h = self._original_image.height + height
        image = self._pil.new(self._original_image.mode, (w, h), fill_color)
        image.paste(self._original_image, (0, 0))
        self._original_image = image
        self._image = self._pil.new("RGBA", image.size)
        return original_w, original_h

    def image_segmentation_overlay(self, conversion, overlay_data, lut):
        """Return an image scaled with respect to the provided image transformation callback with overlay data

        - `conversion`: coordinate conversion function accepting two arguments (x,y) and returning two-element tuple
        - `overlay_data`: overlay data to blend
        - `lut`: overlay data look up table in RGB format
        """
        orig_image = numpy.array(self._original_image)
        orig_height, orig_width = orig_image.shape[:2]
        img = _image_segmentation_overlay(
            conversion, overlay_data, orig_width, orig_height, lut
        )
        img = _create_alpha_channel(img, int(255 * self._alpha))
        self._image = self._pil.fromarray(img)


def _iround(x) -> int:
    """Integer round"""
    return int(x)


class _PrimitivesDrawOpenCV:
    """Drawing class for OpenCV backend"""

    def __init__(self, image, alpha, font_scale):
        """Constructor.

        - image: native image object
        - alpha: alpha-blend weight for overlay details
        - font_scale: font scale to use for overlay details
        """
        self._original_image = image
        self._image = numpy.zeros(image.shape, image.dtype)
        self._alpha = alpha
        self._cv = importlib.import_module("cv2")
        self._font = self._cv.FONT_HERSHEY_PLAIN
        self._font_scale = font_scale

    def _adj_color(self, color):
        return color[::-1]

    def draw_circle(self, cx, cy, radius, width, color, fill=False):
        """Draw circle.

        - px: X coordinate
        - py: Y coordinate
        - radius: circle radius
        - width: line width
        - color: color to use
        - fill: whether to fill the circle
        """

        if fill:
            self._cv.circle(
                self._image,
                (_iround(cx), _iround(cy)),
                _iround(
                    radius + width / 2
                ),  # wider circle to account for 1px thickness
                self._adj_color(color),
                -1,
            )
        else:
            self._cv.circle(
                self._image,
                (_iround(cx), _iround(cy)),
                _iround(radius),
                self._adj_color(color),
                width,
            )

    def text_size(self, text):
        """Calculate text box width, height, and baseline (y-coordinate of the baseline relative to the bottom-most text point).

        - text: text to calculate box size

        Returns tuple containing text width, text height, and baseline
        """
        text_size, baseline = self._cv.getTextSize(
            text, self._font, self._font_scale, 1
        )
        text_w = text_size[0]
        text_h = text_size[1] + baseline
        return (text_w, text_h, baseline)

    def draw_text(self, px, py, color, text):
        """Draw text string.

        - px: X coordinate of upper left point
        - py: Y coordinate of upper left point
        - color: color to use
        - text: text to draw
        """
        px = _iround(px)
        py = _iround(py)
        text_w, text_h, baseline = self.text_size(text)
        self._cv.putText(
            self._image,
            text,
            (px, py + text_h - 2),
            self._font,
            self._font_scale,
            self._adj_color(color),
        )
        return (px, py, px + text_w, py + text_h)

    def draw_text_label(self, x1, y1, x2, y2, color, text, line_width) -> tuple:
        """Draw text label near given rectangular frame so it will be always visible

        - x1: X coordinate of left lower point of frame
        - y1: Y coordinate of left lower point of frame
        - x2: X coordinate of upper right point of frame
        - y2: Y coordinate of upper right point of frame
        - color: color to use
        - text: text to draw

        Returns drawn text label bounding box coordinates
        """

        x1 = _iround(x1)
        x2 = _iround(x2)
        y1 = _iround(y1)
        y2 = _iround(y2)

        margin = 1
        text_w, text_h, baseline = self.text_size(text)
        bbox_w = text_w + 2 * margin
        bbox_h = text_h + baseline + 2 * margin

        half_lw = line_width // 2 + line_width % 2
        if y1 >= bbox_h:
            ty = y1 - bbox_h + margin - half_lw  # above frame top
        elif y2 + bbox_h < self._image.shape[0]:
            ty = y2 + margin + half_lw  # below frame bottom
        else:
            ty = y1 + margin  # below frame top

        if x1 + bbox_w < self._image.shape[1]:
            tx = x1 + margin - half_lw  # from frame left
        elif x2 >= bbox_w:
            tx = x2 - bbox_w + margin + half_lw  # to frame right
        elif self._image.shape[1] >= bbox_w:
            tx = self._image.shape[1] - bbox_w + margin  # to image right
        else:
            tx = margin  # from image left

        bbox = (
            tx - margin,
            ty - margin,
            tx + text_w + margin,
            ty + text_h + baseline + margin,
        )

        self._cv.rectangle(
            self._image, bbox[:2], bbox[-2:], self._adj_color(color), self._cv.FILLED
        )

        text_color = (1, 1, 1) if _luminance(color) > 180 else (255, 255, 255)
        self.draw_text(tx, ty, self._adj_color(text_color), text)
        return bbox

    def draw_line(self, x1, y1, x2, y2, width, color):
        """Draw line.

        - x1: X coordinate of beginning point
        - y1: Y coordinate of beginning point
        - x2: X coordinate of ending point
        - y2: Y coordinate of ending point
        - width: line width
        - color: color to use
        """

        x1 = _iround(x1)
        x2 = _iround(x2)
        y1 = _iround(y1)
        y2 = _iround(y2)

        self._cv.line(self._image, (x1, y1), (x2, y2), self._adj_color(color), width)

    def draw_box(self, x1, y1, x2, y2, width, color):
        """Draw rectangle.

        - x1: X coordinate of left lower point
        - y1: Y coordinate of left lower point
        - x2: X coordinate of upper right point
        - y2: Y coordinate of upper right point
        - width: line width
        - color: color to use
        """
        x1 = _iround(x1)
        x2 = _iround(x2)
        y1 = _iround(y1)
        y2 = _iround(y2)

        self._cv.rectangle(
            self._image, (x1, y1), (x2, y2), self._adj_color(color), width
        )

    def image_overlay(self):
        """Return image overlay with proper blending"""
        mask = self._cv.cvtColor(self._image, self._cv.COLOR_BGR2GRAY) != 0
        ret = self._original_image.copy()
        ret[mask] = (
            self._image[mask] * self._alpha
            + self._original_image[mask] * (1 - self._alpha)
        ).astype(self._original_image.dtype)
        return ret

    def image_overlay_extend(self, width, height, fill_color):
        """Update input image by extending its size.

        - width: width to extend up to
        - height: height value to extend
        - fill_color: color to use use if any form of padding is used

        Returns original image width and height
        """
        original_w = self._original_image.shape[1]
        original_h = self._original_image.shape[0]
        w = max(self._original_image.shape[1], width)
        h = self._original_image.shape[0] + height
        image = numpy.zeros(
            (h, w, self._original_image.shape[2]), self._original_image.dtype
        )
        image[:] = tuple(reversed(fill_color))
        image[
            0 : self._original_image.shape[0], 0 : self._original_image.shape[1], :
        ] = self._original_image
        self._original_image = image
        self._image = numpy.zeros(image.shape, image.dtype)
        return original_w, original_h

    def image_segmentation_overlay(self, conversion, overlay_data, lut):
        """Return an image scaled with respect to the provided image transformation callback with overlay data

        - `conversion`: coordinate conversion function accepting two arguments (x,y) and returning two-element tuple
        - `overlay_data`: overlay data to blend
        - `lut`: overlay data look up table in RGB format
        """
        orig_height, orig_width = self._original_image.shape[:2]
        self._image = _image_segmentation_overlay(
            conversion, overlay_data, orig_width, orig_height, lut
        )


def create_draw_primitives(image_data, alpha, font_scale):
    """Create and return PrimitivesDraw object to use to draw overlays.

    - image-data: inference input image
    - alpha: alpha-blend weight for overlay details
    - font_scale: font scale to use for overlay details
    """
    if (
        isinstance(image_data, numpy.ndarray)
        and len(image_data.shape) == 3
        and importlib.util.find_spec("cv2")
    ):
        return _PrimitivesDrawOpenCV(image_data, alpha, font_scale)

    if importlib.util.find_spec("PIL"):
        pillow = importlib.import_module("PIL")
        if pillow and isinstance(image_data, pillow.Image.Image):
            return _PrimitivesDrawPIL(image_data, alpha, font_scale)

    raise DegirumException("Unknown preprocessed image data format")
