from typing import Any, Tuple
from customtkinter import CTkLabel
from customtkinter.windows.widgets.font import CTkFont
from customtkinter.windows.widgets.image import CTkImage

from .translatable import Translatable
from .translation_manager import TranslationManager

class TLabel(CTkLabel, Translatable):
    """
    ## Translatable Label

    :info: finder key starts with label.
    """
    def __init__(self,
                 master: Any, 
                 translation_manager: TranslationManager,
                 key: str="TLabel", 
                 width: int = 0, height: int = 28, 
                 corner_radius: int | None = None, 
                 bg_color: str | Tuple[str, str] = "transparent", fg_color: str | Tuple[str, str] | None = None, 
                 text_color: str | Tuple[str, str] | None = None, text_color_disabled: str | Tuple[str, str] | None = None, 
                 font: tuple | CTkFont | None = None, 
                 image: CTkImage | None = None, 
                 compound: str = "center", 
                 anchor: str = "center", 
                 wraplength: int = 0, 
                 **kwargs):
        """
        ## Create a Translatable-Label

        :param master: mandatory, same functionality as `Widget.master`.
        :param key: used to let the `TranslationManager` find the correct text value.
        :param width/height: set the width and height of this label. *(not recommended for apps that dynamically scale)
        :param corner_radius: if foreground color is not '`transparent`', makes the edges of this label round.
        :param text_color: color of the text.
        :param font: the font used for the text.
        :param image: if this is not `None` the text is replaced with an image, *(TranslationManager ignores this `text-like`)
        :param compound: unknown
        :param anchor: the anchor used to place this label *(e.g.: if anchor is center and relx is 0.5 the widget is placed in the exact center. very useful)
        :param wraplength: unknown
        """
        super().__init__(master, 
                         width, 
                         height, 
                         corner_radius, 
                         bg_color, 
                         fg_color, 
                         text_color, 
                         text_color_disabled, 
                         "<UpdateTranslationManager, NoLabelTextGiven>", 
                         font, 
                         image, 
                         compound, 
                         anchor, 
                         wraplength, 
                         **kwargs
                         )
        self._translation_key = key
        self.translation_manager = translation_manager
        self.translation_manager._text_likes.update({self._get_translation_key(): self}) # good
        "used internally"
    
    def _get_translation_key(self):
        """helps the TranslationManager find the key more easily"""
        return f"label.{self._translation_key}"

    def _translate(self, value:str):
        """Internal helper-function"""
        self.configure(text=value)