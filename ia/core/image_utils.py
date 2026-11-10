import io

from PIL import Image


def load_image(data: bytes) -> Image.Image:
    buffer = io.BytesIO(data)
    img = Image.open(buffer)
    return img.convert("RGB")
