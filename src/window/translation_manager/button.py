from tkinter import Variable
from typing import Any, Callable, Tuple
from customtkinter import CTkButton
from customtkinter.windows.widgets.font import CTkFont
from customtkinter.windows.widgets.image import CTkImage

from .translatable import Translatable
from .translation_manager import TranslationManager

class TButton(CTkButton, Translatable):
    """
    ## Translapagele Button

    :info: finder key starts with button.
    """
    def __init__(self, 
                 master: Any, 
                 translation_manager: TranslationManager,
                 key: str,
                 width: int = 140, height: int = 28, 
                 corner_radius: int | None = None, 
                 border_width: int | None = None, border_spacing: int = 2, 
                 bg_color: str | Tuple[str, str] = "transparent", fg_color: str | Tuple[str, str] | None = None, 
                 hover_color: str | Tuple[str, str] | None = None, border_color: str | Tuple[str, str] | None = None, 
                 text_color: str | Tuple[str, str] | None = None, text_color_disabled: str | Tuple[str, str] | None = None, 
                 background_corner_colors: Tuple[str | Tuple[str, str]] | None = None, 
                 round_width_to_even_numbers: bool = True, round_height_to_even_numbers: bool = True, 
                 font: tuple | CTkFont | None = None, textvariable: Variable | None = None, 
                 image: CTkImage | Any | None = None, 
                 state: str = "normal", hover: bool = True, 
                 command: Callable[[], Any] | None = None, 
                 compound: str = "left", anchor: str = "center", **kwargs):
        """
        ## Create a Translatable-Button

        :param master: mandatory, same functionality as `Widget.master`.
        :param key: used to let the `TranslationManager` find the correct text value.
        :param width/height: set the width and height of this button. *(not recommended for apps that dynamically scale)
        :param corner_radius: if foreground color is not '`transparent`', makes the edges of this button round.
        :param text_color: color of the text.
        :param font: the font used for the text.
        :param image: if this is not `None` the text is replaced with an image, *(TranslationManager ignores this `text-like`)
        :param compound: unknown
        :param anchor: the anchor used to place this Button *(e.g.: if anchor is center and relx is 0.5 the widget is placed in the exact center. very useful)
        :param wraplength: unknown
        """
        super().__init__(master, 
                         width, height, 
                         corner_radius, 
                         border_width, border_spacing, 
                         bg_color, fg_color, 
                         hover_color, border_color, 
                         text_color, text_color_disabled, 
                         background_corner_colors, 
                         round_width_to_even_numbers, round_height_to_even_numbers, 
                         "<UpdateTranslationManager, NoButtonTextGiven>", font, textvariable, 
                         image, 
                         state, hover, 
                         command, 
                         compound, anchor, **kwargs)
        if "." in key:
            raise ValueError(f"Argument key does not allow periods, key:{key} is not allowed")
        self._translation_key = key
        self.translation_manager = translation_manager
        self.translation_manager._text_likes.update({self._get_translation_key(): self}) # good
        "used internally"
    
    def _get_translation_key(self):
        """helps the TranslationManager find the key more easily"""
        return f"button.{self._translation_key}"

    def _translate(self, value:str):
        """Internal helper-function"""
        self.configure(text=value)