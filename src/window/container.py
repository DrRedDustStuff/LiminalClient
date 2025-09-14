import base64, json

"""Container for settings and such"""

class Settings:
    def __init__(self, file) -> None:
        with open(f"files/{file}", "r") as f:
            data:list[str] = f.readlines()
        self.lang: str = data[0]
        self.user = "Neon" #json.loads(data[1])
        if not isinstance(self.user, dict):
            self.user = {"User":"None"}