from blublib import log

def interpret(path:str) -> dict[str, str]:
    src = ""
    with open(path, "r", encoding="utf-8") as rlf:
        src = rlf.read()
        rlf.close()

    keyvalue: dict[str,str] = {}
    lns = src.split("\n")
    for i,line in enumerate(lns):
        line = line.split("//")[0].strip()
        if line == "": continue
        try:
            k,v = line.split(":",1)
            key = k.strip()
            value = v.strip()
            if len(value) >= 2:
                if value[0] == '"' and value[-1] == '"': value = value[1:-1]
                if value in keyvalue.keys(): value = keyvalue[value]
            keyvalue.update({key:value})
        except ValueError as ve:
            log.error("Error at line %s of file %s, perhaps you forgot a colon?"%(i,path))

    return keyvalue

def create(path:str,keyvvalue:dict[str,str]) -> dict[str, str]:
    src = ""
    for key,value in keyvvalue.items():
        src += '%s:"%s"'%(key,value)

    with open(path,"w", encoding="utf-8") as wlf:
        wlf.write(src)
        wlf.close()

    return keyvvalue