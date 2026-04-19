
keys = [
    "\t" + str(tuple( i.split(",", 1) ))
        for i in open("datagen/keys.txt","r", encoding="utf-8").read().split("\n")]

with open("./src/datagen.py", "w", encoding="utf-8") as fw:
    lines = [
        "########################",
        "# Generated in datagen #",
        "########################\n",
        "keys: list[tuple[str,str]] = [",
        ",\n".join(keys),
        "]"
    ]

    text = ""
    for line in lines:
        text += line + "\n"

    fw.write(text)

from PIL import Image

Image.open("./resources/images/Icon.png").save("./resources/icon.ico")
