import base64
import io

import cv2
import numpy as np
from pdf2image import convert_from_bytes
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


def str_to_img(img_str: str) -> np.array:
    """converts b64 img to np.array"""
    img_data = base64.b64decode(img_str)
    img_arr = np.fromstring(img_data, np.uint8)
    img = cv2.imdecode(img_arr, cv2.IMREAD_COLOR)
    return img


def read_form_img(img_str: str) -> np.array:
    """reads image from web form"""
    img_arr = np.fromstring(img_str, np.uint8)
    img = cv2.imdecode(img_arr, cv2.IMREAD_COLOR)
    return img


def pdf_upload_to_img(pdf) -> np.ndarray:
    image = convert_from_bytes(pdf.read())[0]
    np_img = np.array(image)
    cv_img = cv2.cvtColor(np_img, cv2.COLOR_RGB2BGR)
    return cv_img
