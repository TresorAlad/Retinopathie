import io

import pytest
from PIL import Image

from core.constants import STAGE_LABELS
from core.image_utils import load_image


def make_image_bytes(width=300, height=300, color=(128, 60, 60)):
    img = Image.new("RGB", (width, height), color)
    buffer = io.BytesIO()
    img.save(buffer, format="JPEG")
    buffer.seek(0)
    return buffer.read()


def test_load_image_returns_pil_rgb():
    img = load_image(make_image_bytes())
    assert img.mode == "RGB"
    assert img.size == (300, 300)


def test_load_image_raises_on_invalid_bytes():
    with pytest.raises(Exception):
        load_image(b"pas une image")


def test_stage_labels_complete():
    assert set(STAGE_LABELS.keys()) == {0, 1, 2, 3, 4}
