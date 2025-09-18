# Based on Minecraft Styling Functionality

# {"text":"TEXT", "color":"black/red/green/yellow/blue/magenta/cyan/white", "style":"normal/bold/dim/italic/underline/blink/inverse"}
# or in list format
# ->
# \033[<style_code>;<color_code>m<text>\033[0m

# TODO:
# Handle BBCode Format
# Parse -> Interpret

# no printing just interpreting

COLOR = {
    "black":30,
    "red":31,
    "green":32,
    "yellow":33,
    "blue":34,
    "magenta":35,
    "cyan":36,
    "white":37
}

STYLE = {
    "normal":0,
    "bold":1,
    "dim":2,
    "italic":3,
    "underline":4,
    "blink":5,
    "inverse":7
}

def handle_single(frame:dict[str, str]):
    text = frame.get("text", "<MissingText>")
    color = COLOR[frame.get("color", "white")]
    style = STYLE[frame.get("style", "normal")]

    return f"\033[{style};{color}m{text}\033[0m"

def handle_multiple(frames:list[dict[str,str]]):
    result = ""
    for frame in frames:
        result += handle_single(frame)
    return result