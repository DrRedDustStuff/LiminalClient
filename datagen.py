from typing import Any
from liminal_client import log

from PIL import Image
from PIL import ImageDraw

mode = "RGBA"
icon = Image.new(mode, (500,500))
icon_draw = ImageDraw.Draw(icon,mode)

grp = "#000000", 20
icon_draw.rectangle(((150,150),(500,500)), "#bdc54d", *grp)
icon_draw.polygon(((0,0),(500,0),(500,150),(150,150)),"#b5c8d1", *grp)
icon_draw.polygon(((0,0),(0,500),(150,500),(150,150)),"#db9f30", *grp)

icon.save("./resources/image/icon.png")
icon.save("./resources/image/icon.ico")



