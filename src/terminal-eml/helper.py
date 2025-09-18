import os, platform, sys

def set_terminal_size(columns:int, rows:int):
    sys_name = platform.system()
    if sys_name == "Windows":
        os.system(f"mode con: cols={columns} lines={rows}")
    elif sys_name in ["Linux", "Darwin"]:
        os.system(f"stty cols {columns} rows {rows}")
    else:
        raise OSError(f"Unsupported operating system: {sys_name}. Sorry to lazy to add that one :D")
        
def change_terminal_cursor(style:int):
    """
    Set the Terminal cursor style
    
    Common Styles:
    <br>0 - Blinking Block
    <br>1 - Blinking Block (default)
    <br>2 - Steady Block
    <br>3 - Steady Underline
    <br>4 - Blinking Bar
    <br>5 - Steady Bar
    """
    sys.stdout.write(f"\033[{style} q")
    sys.stdout.flush()
    print("changed terminal cursor")