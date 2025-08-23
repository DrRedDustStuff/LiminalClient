import mistune
import json
from os import getcwd
from os.path import join

cwd = getcwd()

md = mistune.create_markdown(renderer="ast")
ast = md.read(join(cwd, "test.md"))

print(join(cwd, "test.md"))

if isinstance(ast[0], list):
    print(json.dumps(ast[0], indent=2))