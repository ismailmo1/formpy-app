import base64
import io

import cv2
import formpy.utils.img_processing as ip
import numpy as np
from PIL import Image


def thresh_img(img: np.array):
    """test func to render images"""
    img = Image.fromarray(ip.thresh_img(img))
    img_buf = io.BytesIO()
    img.save(img_buf, "PNG")
    img_buf.seek(0)
    img_base64 = base64.b64encode(img_buf.read())
    return str(img_base64).split("'")[1]


def read_img(img_str):
    """reads image from web form"""
    img_arr = np.fromstring(img_str, np.uint8)
    img = cv2.imdecode(img_arr, cv2.IMREAD_COLOR)
    return img
