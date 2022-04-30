import cv2
import numpy as np
from numpy.testing import assert_array_equal


def test_order_pts():
    from app.formpyapp.api.alignment import order_pts

    unordered_pts = np.array(
        [
            [2322.0, 75.0],
            [110.0, 76.0],
            [110.0, 1575.0],
            [2322.0, 1575.0],
        ]
    )
    ordered_pts = order_pts(unordered_pts)

    assert_array_equal(
        [[110.0, 76.0], [2322.0, 75.0], [2322.0, 1575.0], [110.0, 1575.0]],
        ordered_pts,
    )


def test_align_img():
    from app.formpyapp.api.alignment import align_img

    # use png for lossless save
    test_img = cv2.imread("tests/artifacts/images/simple_qna_aligned.png")
    misaligned_img = cv2.imread(
        "tests/artifacts/images/simple_qna_misalign.jpeg"
    )

    aligned_img = align_img(misaligned_img)

    assert_array_equal(aligned_img, test_img)


def test_get_bounding_pts(simple_qna_img):
    from app.formpyapp.api.alignment import get_bounding_pts

    pts = get_bounding_pts(simple_qna_img)

    assert_array_equal(
        [[110.0, 76.0], [2322.0, 75.0], [2322.0, 1575.0], [110.0, 1575.0]], pts
    )


def test_add_align_rectangle(simple_qna_img):
    from app.formpyapp.api.alignment import add_align_rectangle

    test_img = cv2.imread("tests/artifacts/images/align_border.png")

    blank_img = np.full_like(simple_qna_img, 255)
    bordered_img = add_align_rectangle(blank_img)

    assert_array_equal(bordered_img, test_img)
