import cv2
from numpy.testing import assert_array_equal
from werkzeug.datastructures import FileStorage


def test_img_to_str(simple_qna_img):
    from app.formpyapp.api.img_proc import img_to_str

    with open("tests/artifacts/img_to_str.txt") as f:
        str_img = f.read()

    assert img_to_str(simple_qna_img) == str_img


def test_str_to_img(simple_qna_img):
    from app.formpyapp.api.img_proc import str_to_img

    with open("tests/artifacts/img_to_str.txt") as f:
        str_img = f.read()

    assert_array_equal(str_to_img(str_img), simple_qna_img)


def test_read_form_img(simple_qna_img):
    from app.formpyapp.api.img_proc import read_form_img

    with open("tests/artifacts/images/simple_qna.jpeg", "rb") as f:
        img_bytes = f.read()

    img_from_bytes = read_form_img(img_bytes)

    assert_array_equal(simple_qna_img, img_from_bytes)


def test_pdf_to_jpeg():
    from app.formpyapp.api.img_proc import pdf_upload_to_img

    with open("tests/artifacts/pdf/simple_qna.pdf", "rb") as f:
        pdf_file = FileStorage(f)
        converted_img = pdf_upload_to_img(pdf_file)

    # use png to ensure lossless write
    test_img = cv2.imread("tests/artifacts/images/pdf_conversion.png")
    assert_array_equal(test_img, converted_img)
