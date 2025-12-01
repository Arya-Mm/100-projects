import pytest
from PIL import Image
from resizer import resize_image, apply_watermark

def test_resize_image():
    img = Image.new("RGB", (1000, 500))
    out = resize_image(img, 500, None)  # width only
    assert out.width == 500
    assert out.height == 250

def test_resize_image_height():
    img = Image.new("RGB", (1000, 500))
    out = resize_image(img, None, 250)  # height only
    assert out.height == 250
    assert out.width == 500

def test_watermark():
    img = Image.new("RGB", (800, 600))
    out = apply_watermark(img, "Test Watermark")
    assert out.size == img.size
