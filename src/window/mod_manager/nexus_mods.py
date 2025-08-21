from typing import Any, Optional
from PIL.ImageFile import ImageFile
import requests
import os
from requests import Response
from PIL import Image
from io import BytesIO

API_KEY  = "A6W4RZ8gnUeHyShkZObUhZR1LPI6EWjaHhijGUHdFpv8vmQ=--bX4PWJ4uDEEXqUJZ--a5EdEqnexUXb6OdM7n/Dgw=="
BASE_URL = "https://api.nexusmods.com/v1/"
GAME     = "escapethebackrooms"

class NexusMods:
    def __init__(self, game_url_name:str, api_key:str, app_name:str = "APPNAME") -> None:
        self.game = game_url_name
        self.api_key = api_key
        self.app_name = app_name
        self.response: Response = Response()
        self.headers = {
            "apikey": self.api_key,
            "Application-Name": app_name
        }
    
    def fetch_trending(self, amount:Optional[int] = None) -> list[dict[str, Any]]:
        self.response = requests.get(BASE_URL + f"games/{self.game}/mods/trending.json", headers=self.headers)
        if self.response.status_code != 200:
            raise Exception(f"API request failed: {self.response.status_code}")
        
        jsn:list[dict[str, Any]] = self.response.json()
        if amount:
            return jsn[:amount]
        else:
            return jsn
    
    def fetch_latest_added(self, amount:Optional[int] = None) -> list[dict[str, Any]]:
        self.response = requests.get(BASE_URL + f"games/{self.game}/mods/latest_added.json", headers=self.headers)
        if self.response.status_code != 200:
            raise Exception(f"API request failed: {self.response.status_code}")
        
        jsn:list[dict[str, Any]] = self.response.json()
        if amount:
            return jsn[:amount]
        else:
            return jsn
        
    def fetch_latest_updated(self, amount:Optional[int] = None) -> list[dict[str, Any]]:
        self.response = requests.get(BASE_URL + f"games/{self.game}/mods/latest_updated.json", headers=self.headers)
        if self.response.status_code != 200:
            raise Exception(f"API request failed: {self.response.status_code}")

        jsn:list[dict[str, Any]] = self.response.json()
        if amount:
            return jsn[:amount]
        else:
            return jsn
    
    def fetch_by_id(self, id:int) -> dict[str, Any]:
        self.response = requests.get(BASE_URL + f"games/{self.game}/mods/{id}.json", headers=self.headers)
        if self.response.status_code != 200:
            raise Exception(f"API request failed: {self.response.status_code}")
        
        return self.response.json()

    def download_file(self, url, folder_path, filename=None):
        """
        Downloads a file from a URL to a specific folder.

        :param url: URL of the file to download
        :param folder_path: Folder to save the file
        :param filename: Optional custom filename (default: from URL)
        """
        # Create the folder if it doesn’t exist
        os.makedirs(folder_path, exist_ok=True)

        # Use filename from URL if not provided
        if not filename:
            filename = url.split('/')[-1] or "downloaded_file"

        # Full path
        file_path = os.path.join(folder_path, filename)

        try:
            # Send GET request
            response = requests.get(url, stream=True)
            response.raise_for_status()

            # Save file in chunks
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

            print(f"✅ Downloaded: {file_path}")
            return file_path

        except requests.exceptions.RequestException as e:
            print(f"❌ Failed to download: {e}")
            return None
    
def load_mod_image(mod_jsn:dict[str, Any]) -> ImageFile:
    response = requests.get(mod_jsn["picture_url"])
    response.raise_for_status()
    return Image.open(BytesIO(response.content))

nm = NexusMods(GAME, API_KEY, "Neo-EML")

print(nm.fetch_by_id(7))