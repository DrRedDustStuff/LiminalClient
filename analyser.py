# Analyze and find any imported libraries
#
#

from types import ModuleType
from typing import Mapping, Sequence

import log
import sys
import os

imported: set[str] = set()
queue_import: list[str] = []

def handle_import(lines: list[str], idx: int):
    print(lines[idx])

def handle_from(lines: list[str], idx: int):

    x0 = lines[idx].removesuffix("\n").split(" ")
    from_path = x0[1].replace(".","/")
    import_item = x0[3] + ".py"

    import_items = []

    if import_item.startswith("("):
        raise Exception("Multi line imports not supported yet")
    else:
        import_items = import_item.split(",")

    log.message(
        log.style("From ", "green"),
        log.style(from_path),
        log.style(" Import ", "green"),
        log.style(", ".join(import_items)),
    )

    for path in sys.path:
        fp = os.path.join(path, from_path)
        if os.path.exists(fp):
            queue_import.append(os.path.join)
    

def execute_and_find_imports(file: str):
    with open(file, "r", encoding="utf-8") as rpf:
        lines = rpf.readlines()
        for i,line in enumerate(lines):
            if line.strip().startswith("import"):
                handle_import(lines, i)
            elif line.strip().startswith("from"):
                handle_from(lines, i)
        rpf.close()

queue_import.append("main.py")

while len(queue_import) > 0:
    imp = queue_import.pop(0)
    if imp in imported: continue
    execute_and_find_imports(imp)