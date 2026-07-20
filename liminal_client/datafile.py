class Property[T]:
    def __init__(self,value:T,bytes:int) -> None:
        self.value = value
        self.bytes = bytes

    def get(self) -> bytes:
        if hasattr(self.value,"to_bytes"):
            return self.value.to_bytes(self.bytes) # pyright: ignore[reportAttributeAccessIssue]
        elif T == str:
            return self.value.encode()[0:self.bytes] # pyright: ignore[reportAttributeAccessIssue]
        else:
            raise Exception("Object '%s' of type '%s' does not have the necessary functions for bytes conversion"%(self.value,T))

    def set(self,b:bytes):
        if hasattr(T,"from_bytes"):
            self.value = T.from_bytes(b) # pyright: ignore[reportAttributeAccessIssue]
        elif T == str:
            self.value = b.decode() # pyright: ignore[reportAttributeAccessIssue]
        else:
            raise Exception("Object '%s' of type '%s' does not have the necessary functions for bytes conversion"%(self.value,T))

import os

class Datafile:
    def __init__(self,path:str) -> None:
        self.path = path
        self.properties: dict[str,Property] = {}

        if not os.path.exists(path):
            with open(self.path,"xb") as create:
                create.write(b"")
                create.close()

    def read(self):
        with open(self.path,"rb") as rdfb:
            bin = rdfb.read()
            offset = 0
            for k,v in self.properties.items():
                binary = bin[offset:v.bytes]
                self.properties[k].set(binary)
                offset += v.bytes
            rdfb.close()

    def write(self):
        with open(self.path,"wb") as wdfb:
            bin = bytes()
            bin += b"DATAFILE"
            for k,v in self.properties.items():
                bin += v.get()
            wdfb.write(bin)
            wdfb.close()

    def boolean(self, name:str,v:bool):
        self.create_boolean(name)
        self.set_boolean(name,v)
        return self
    def integer(self, name:str,v:int,  bytes:int):
        self.create_integer(name,bytes)
        self.set_integer(name,v)
        return self
    def floating(self,name:str,v:float,bytes:int): ...
    def string(self,  name:str,v:str,  bytes:int):
        self.create_string(name,bytes)
        self.set_string(name,v)
        return self

    def create_boolean(self,name:str           ): self.properties.update({name:Property[bool](False,1)})
    def create_integer(self,name:str, bytes:int): self.properties.update({name:Property[int](0,bytes)})
    def create_floating(self,name:str,bytes:int): self.properties.update({name:Property[float](0.0,bytes)})
    def create_string(self,name:str,  bytes:int): self.properties.update({name:Property[str]("",bytes)})
    
    def set_boolean(self,name:str,v:bool  ): self.properties[name].value = v
    def set_integer(self,name:str,v:int   ): self.properties[name].value = v
    def set_floating(self,name:str,v:float): self.properties[name].value = v
    def set_string(self,name:str,v:str    ): self.properties[name].value = v

    def get_boolean(self,name:str ) -> bool:  return self.properties[name].value # pyright: ignore[reportReturnType]
    def get_integer(self,name:str ) -> int:   return self.properties[name].value # pyright: ignore[reportReturnType]
    def get_floating(self,name:str) -> float: return self.properties[name].value # pyright: ignore[reportReturnType]
    def get_string(self,name:str  ) -> str:   return self.properties[name].value # pyright: ignore[reportReturnType]

