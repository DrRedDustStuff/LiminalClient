import requests

API_KEY = "A6W4RZ8gnUeHyShkZObUhZR1LPI6EWjaHhijGUHdFpv8vmQ=--bX4PWJ4uDEEXqUJZ--a5EdEqnexUXb6OdM7n/Dgw=="
BASE_URL = "https://api.nexusmods.com/v1/"
GAME = "escapethebackrooms"

headers = {
    "apikey": API_KEY,
    "Application-Name": "Neo-EML"
}

response = requests.get(BASE_URL + f"games/{GAME}/mods/trending.json", headers=headers)

if response.status_code == 200:
    mods = response.json()
    for mod in mods[:5]:
        print(f"{mod["mod_id"]}: {mod["name"]} - by {mod["user"]["name"]}")
else:
    print("Error:",response.status_code,response.text)