import json

import app.formpy.utils.img_processing as ip
import cv2
import numpy as np


def order_pts(pts: np.ndarray):
    """return ordered points of rectangle ordered from top left clockwise"""
    ordered_pts = np.zeros((4, 2), dtype="float32")
    ordered_pts[0] = pts[np.argmin(pts.sum(axis=1))]
    ordered_pts[2] = pts[np.argmax(pts.sum(axis=1))]

    # smallest difference x-y = top right
    ordered_pts[1] = pts[np.argmin(np.diff(pts, axis=1))]
    # largest difference x-y = bottom left
    ordered_pts[3] = pts[np.argmax(np.diff(pts, axis=1))]
    return ordered_pts


def align_img(img: np.array, json_pts: str = None) -> np.array:
    """aligns image with bounding box if detected

    Args:
        img (np.array): user uploaded image

    Returns:
        np.array: aligned image
    """
    if json_pts is not None:
        pts = np.array(json.loads(json_pts), dtype="float32")
        ordered_pts = order_pts(pts)
    else:
        ordered_pts = None
    aligned_img = ip.align_page(img, corner_pts=ordered_pts)

    return aligned_img


def get_bounding_pts(img: np.ndarray) -> tuple:
    pts = ip.get_outer_box(img)
    return pts


def add_align_rectangle(img):
    """add rectangle to border of image

    Args:
        img (np.ndarray): aligned

    Returns:
        img (np.ndarray): aligned image with black border
    """
    # add buffer of 2 to ensure border isn't cut off from img
    cv2.rectangle(
        img,
        pt1=(20, 20),
        pt2=(img.shape[1] - 20, img.shape[0] - 20),
        color=(0, 0, 0),
        thickness=20,
    )

    return img
