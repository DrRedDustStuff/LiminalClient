from xml.dom import minidom
from PIL import Image, ImageDraw, ImageMode
from typing import cast


def _default(name: str, value: str):
    attr = minidom.Attr(name)
    attr.value = value
    return attr


def _trans_single(x: float, rw: int, w: int):
    return (x / rw) * w


def _transform(pos: tuple[float,float], rsize: tuple[int,int], size: tuple[int,int]):
    return _trans_single(pos[0],rsize[0],size[0]),_trans_single(pos[1],rsize[1],size[1])


# To implement
# (Required for LiminalClient)
# - circle
# - polygon
# - path
# - polyline
# - line
def draw_svg(element: minidom.Element, draw: ImageDraw.ImageDraw, size: tuple[int,int], rsize: tuple[int,int], env: dict):
    match element.nodeName:
        case "circle":
            cx = float(element.getAttribute("cx"))
            cy = float(element.getAttribute("cy"))
            r = float(element.getAttribute("r"))
            
            draw.circle(
                _transform((cx,cy),rsize,size),
                _trans_single(r,rsize[0],size[0]), 
                env["fill"] if env["fill"] != "none" else None, 
                env["stroke"], 
                round(_trans_single(float(env["stroke-width"]), rsize[0], size[0]))
            )
        case "polygon":
            points: list[tuple[float,float]] = []
            raw = element.getAttribute("points").split(" ")
            num = len(raw)//2
            for i in range(num):
                idx = i*2
                points.append(_transform(
                    (
                        float(raw[idx+0]),
                        float(raw[idx+1])
                    ),
                    rsize,
                    size
                ))

            draw.polygon(
                points,
                env["fill"] if env["fill"] != "none" else None,
                env["stroke"],
                round(_trans_single(float(env["stroke-width"]), rsize[0], size[0]))
            )

        case "path":
            print(element.nodeName, element.attributes.items())

            raw = [i for i in element.getAttribute("d")]

            pos = (0.0,0.0)

            def collect_vec2():
                x = ""
                y = ""
                for char in raw:
                    if char == " ":
                        x = y
                        y = ""
                    elif char.isnumeric() or char == ".":
                        y += char

                return float(x),float(y)

            def collect_float():
                x = ""
                for char in raw:
                    if char == " ":
                        break
                    elif char.isnumeric() or char == ".":
                        x += char
                return float(x)

            def add(a: tuple[float,float], b: tuple[float,float], is_local: bool):
                return (
                    (a[0] if not is_local else 0) + b[0],
                    (a[1] if not is_local else 0) + b[1]
                )

            while len(raw) > 0:
                char = raw.pop(0)
                is_local = char.islower()

                match char.upper():
                    case "M":
                        v = collect_vec2()
                        pos = v
                    case "L":
                        draw.line(
                            (
                                _transform(pos, rsize, size),
                                _transform(add(pos,collect_vec2(),is_local),rsize,size)
                            ),
                            env["stroke"],
                            round(_trans_single(float(env["stroke-width"]), rsize[0], size[0])),
                        )
                    case "H":
                        draw.line(
                            (
                                _transform(pos, rsize, size),
                                _transform(add(pos,(collect_float(),0),is_local),rsize,size)
                            ),
                            env["stroke"],
                            round(_trans_single(float(env["stroke-width"]), rsize[0], size[0])),
                        )
                    case "V":
                        draw.line(
                            (
                                _transform(pos, rsize, size),
                                _transform(add(pos,(0,collect_float()),is_local),rsize,size)
                            ),
                            env["stroke"],
                            round(_trans_single(float(env["stroke-width"]), rsize[0], size[0])),
                        )

                    case _: pass

            # ill implement this later
            pass
        case "polyline":
            points: list[tuple[float,float]] = []
            raw = element.getAttribute("points").split(" ")
            num = len(raw)//2
            for i in range(num):
                idx = i*2
                points.append(_transform(
                    (
                        float(raw[idx+0]),
                        float(raw[idx+1])
                    ),
                    rsize,
                    size
                ))

            draw.line(
                points,
                env["stroke"],
                round(_trans_single(float(env["stroke-width"]), rsize[0], size[0])),
                "curve"
            )

        case "line":
            x1 = float(element.getAttribute("x1"))
            y1 = float(element.getAttribute("y1"))
            x2 = float(element.getAttribute("x2"))
            y2 = float(element.getAttribute("y2"))

            draw.line(
                (
                    _transform((x1,y1), rsize, size),
                    _transform((x2,y2), rsize, size)
                ),
                env["stroke"],
                round(_trans_single(float(env["stroke-width"]), rsize[0], size[0]))
            )

        case "#text": pass # ignore text
        case _:
            print(element.nodeName,"Not implemented. dump:",element)


def generate_svg(path: str, size: tuple[int,int], environment: dict):
    "Generates an image based on svg data inside path, using variables from environment"
    file = open(path)

    doc = minidom.parse(file)
    root = doc.getElementsByTagName("svg")[0]

    width, height = size
    rwidth, rheight = int(root.getAttribute("width")),int(root.getAttribute("height"))

    img = Image.new("RGBA", size)
    draw = ImageDraw.Draw(img)

    env = {}

    for k,v in root.attributes.items():
        # print(k,v,v in environment.keys())
        env.update({k:v})
        for rep,rev in environment.items():
            if v != rep: continue
            env.update({k:rev})

    print(env)

    for child in root.childNodes:
        draw_svg(cast(minidom.Element,child),draw, (width,height), (rwidth,rheight), env)

    return img

def direct_generate(string: str, size: tuple[int,int], environment: dict):
    "Generates an image based on svg data inside string, using variables environment"

    doc = minidom.parseString(string)
    root = doc.getElementsByTagName("svg")[0]

    width, height = size
    rwidth, rheight = int(root.getAttribute("width")),int(root.getAttribute("height"))

    img = Image.new("RGBA", size)
    draw = ImageDraw.Draw(img)

    env = {}

    for k,v in root.attributes.items():
        # print(k,v,v in environment.keys())
        env.update({k:v})
        for rep,rev in environment.items():
            if v != rep: continue
            env.update({k:rev})

    print(env)

    for child in root.childNodes:
        draw_svg(cast(minidom.Element,child),draw, (width,height), (rwidth,rheight), env)

    return img
