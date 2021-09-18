import base64
import io
from typing import Tuple

import cv2
import formpy.utils.img_processing as ip
import numpy as np
from formpy.utils.template_definition import find_spots
from PIL import Image


def img_to_str(img: np.array) -> str:
    """writes numpy array img to str

    Args:
        img (np.array): numpy array representation of image

    Returns:
        str: base64 string of image
    """
    img = Image.fromarray(img)
    img_buf = io.BytesIO()
    img.save(img_buf, "PNG")
    img_buf.seek(0)
    img_base64 = base64.b64encode(img_buf.read())
    return str(img_base64).split("'")[1]


def mark_spots(img: np.array) -> Tuple[list[list[int]], np.array]:
    """marks detected spots on template image

    Args:
        img (np.array): image returned from read_img

    Returns:
        np.array: img with bounding boxes around detected spots
    """
    processed_img = ip.process_img(img)
    spot_coords = find_spots(processed_img)
    color_img = cv2.cvtColor(processed_img, cv2.COLOR_GRAY2BGR)
    for i, (x, y) in enumerate(spot_coords):
        cv2.putText(
            color_img,
            str(i),
            (x, y),
            cv2.FONT_HERSHEY_COMPLEX,
            0.7,
            (255, 0, 0),
            1,
        )
        cv2.rectangle(
            color_img, (x - 13, y - 13), (x + 13, y + 13), (255, 0, 0), 2
        )

    return spot_coords, color_img


def str_to_img(img_str: str) -> np.array:
    """reads image from web form"""
    img_arr = np.fromstring(img_str, np.uint8)
    img = cv2.imdecode(img_arr, cv2.IMREAD_COLOR)
    return img
