from typing import Any
from liminal_client import log

from PIL import Image
from PIL import ImageDraw

mode = "RGBA"
icon = Image.open("./resources/image/icon.png")

icon.save("./resources/image/icon.ico")

