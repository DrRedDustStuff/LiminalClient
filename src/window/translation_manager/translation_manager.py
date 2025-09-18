import json
import sys
from typing import Any

class TranslationDict(dict[str, str]):
    """Do not use"""
    def get_key(self, key:str):
        return self.get(key, "<KeyNotFound>")

class TranslationManager:
    """
    ### Keeps track of translation files and makes changes to `TextLike` Widgets,
    widgets are created **from** this to a dict and placed from this classes dict
    *Note: uses a similar approach as minecraft does it with its translation files
    """
    def __init__(self, lang:str="en", translation_folder:str="") -> None:
        """
        ### Create a TranslationManager class to auto update you widgets with the correct language

        :param lang: the starting language, defaults to '`en`'.
        :param translation_folder: the folder with all translation files. *(translation files are json.str_str pairs)
        """
        self._lang: str = lang
        self._lang_data: dict[str, Any] = {}
        "used internally"
        self._translation_folder: str = translation_folder
        "used internally"
        self._text_likes:dict[str, Any] = {}
        with open(f"{self._translation_folder}/{lang}.json") as f:
            self._lang = lang
            self._lang_data = json.load(f)
    
    def get_old(self, key:str):
        """gets a `TextLike` from the dict using the full-key of that `TextLike`
        <br>you can find the full-key from the widgets description"""
        if key in self._text_likes:
            return self._text_likes[key]
        else:
            raise ValueError(f"key not in dict, key:{key}")
    
    def switch_lang(self, new_lang:str="en"):
        """**switches the language to `new_lang`**
        <br>`new_lang` *lang*: new language to be used
        <br> make sure to update text likes for changes to take effect"""
        with open(f"{self._translation_folder}/{new_lang}.json", "r", encoding="ascii") as f:
            self._lang = new_lang
            self._lang_data = json.load(f)
    
    def get_raw(self, key:str):
        """gets raw string translation data"""
        return self._lang_data.get(key, f"<No-{key}-Key>")
    
    def decode(self, text:str):
        result = ""
        i = 0
        while i < len(text):
            char = text[i]
            if char == "/":
                result += (rb"\x" + bytes(text[i+1:i+3])).decode() # type: ignore
                i += 2
            else:
                result += char
            i += 1

        print(result)
        return result

    def update_text_likes(self):
        """Updates all stored `TextLike` widgets to the lang data"""
        for k, w in self._text_likes.items():
            if not w._image is None:
                w.configure(text="")
                continue
            if not hasattr(w, "_get_translation_key"):
                raise ValueError(f"object {k} is not a TextLike &| Translatable")
            key = w._get_translation_key()
            text = self._lang_data.get(key)
            if text is None:
                print(f"key not found:{key}, defaulting to <Default>.")
                w._translate("<Default>")
                continue
            w._translate(text.encode("utf-8"))
            print(text.encode("utf-8"))
            print(f"TextLike:{k} updated to lang: {self._lang}")