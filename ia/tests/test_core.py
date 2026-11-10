import io

import pytest
import torch
from PIL import Image

from core.image_utils import load_image, to_tensor, IMG_SIZE
from core.stage_classifier import STAGE_LABELS


def make_image_bytes(width=300, height=300, color=(128, 60, 60)):
    img = Image.new("RGB", (width, height), color)
    buffer = io.BytesIO()
    img.save(buffer, format="JPEG")
    buffer.seek(0)
    return buffer.read()


def test_load_image_returns_pil_rgb():
    raw = make_image_bytes(300, 300)
    img = load_image(raw)
    assert isinstance(img, Image.Image)
    assert img.mode == "RGB"
    assert img.size == (300, 300)


def test_load_image_handles_rgba():
    img = Image.new("RGBA", (100, 100), (255, 0, 0, 128))
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    result = load_image(buffer.read())
    assert result.mode == "RGB"


def test_load_image_raises_on_invalid_bytes():
    with pytest.raises(Exception):
        load_image(b"ceci n'est pas une image")


def test_to_tensor_shape():
    img = Image.new("RGB", (300, 300), (128, 60, 60))
    tensor = to_tensor(img)
    assert isinstance(tensor, torch.Tensor)
    assert tensor.shape == (1, 3, IMG_SIZE, IMG_SIZE)
    assert tensor.min() < 0.0
    assert tensor.max() > 0.0


def test_to_tensor_accepts_any_input_size():
    for size in [(100, 100), (512, 384), (1024, 1024)]:
        img = Image.new("RGB", size, (100, 100, 100))
        tensor = to_tensor(img)
        assert tensor.shape == (1, 3, IMG_SIZE, IMG_SIZE)


def test_stage_labels_complete():
    assert set(STAGE_LABELS.keys()) == {0, 1, 2, 3, 4}
    assert STAGE_LABELS[2] == "Modérée"
