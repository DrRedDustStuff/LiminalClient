import tkinter
from tkinter import Variable
from tkinter.constants import NORMAL
from typing import Any, Callable, List, Literal, Tuple, cast
from PIL.Image import Image
from typing_extensions import Literal
from deprecated import deprecated

from customtkinter.windows.widgets import (
    CTkButton,
    CTkCheckBox,
    CTkComboBox,
    CTkEntry,
    CTkFrame,
    CTkLabel,
    CTkOptionMenu,
    CTkProgressBar,
    CTkRadioButton,
    CTkScrollbar,
    CTkSegmentedButton,
    CTkSlider,
    CTkSwitch,
    CTkTabview,
    CTkTextbox,
    CTkScrollableFrame,
    CTkGIF,
)
from customtkinter.windows.widgets.font import CTkFont
from customtkinter.windows.widgets.image import CTkImage
from .ui_manager import WidgetManager
from .widget_type import WidgetType
from ..resource import Identifier

from typing import Self, Any

def identifier(id:Identifier,t:Any,postfix:str=""):
    return id.getNamespace() + "." + id.getPath() + ("." + postfix if postfix != "" else "") + "." + type(t).__name__.lower()

def _stringify(val:str|Identifier,t:Any):
    if isinstance(val,str):
        return val
    else:
        return identifier(val,t)
    
# inject for Widgets
class Widget(WidgetType):
    def reg(self, translatable: bool, key: str | Identifier | List[str] | List[Identifier] | None = None, translate_config: str = "text"):
        self._id = 0
        self._translatable = translatable
        self._tc = translate_config
        WidgetManager.add(self)
        if self._translatable:
            if isinstance(key,Identifier):
                key = identifier(key,self)
            elif isinstance(key,List):
                if isinstance(key[0], Identifier):
                    key = [identifier(k,self, "item") for i,k in enumerate(cast(List[Identifier],key))]
            self._key = key
            self.id(key if isinstance(key,str) else cast(str,key[0]))
        self.master = self.master
        self.tag(str(type(self.__class__)))

    def tag(self, tag: str) -> Self:
        WidgetManager.tag(tag, self)
        return self

    def id(self, id: str | Identifier) -> Self:
        WidgetManager.id(_stringify(id,self), self)
        return self

    def add_children(self, ch: "list[Widget]"):
        for child in ch:
            child.pack_configure({"in": self})
            child.master = self
            child._draw()
        return self

    def is_literal(self, val:bool, key:str|None=None):
        self._translatable = not val
        if not val: self._key = key
        return self

    def __repr__(self) -> str:
        return "<%s %s %s>"%(type(self).__name__, self._key if self._key else ".", self.master)


class Button(CTkButton, Widget):
    def __init__(
        self,
        master: Any = None,
        width: int = 140,
        height: int = 28,
        corner_radius: int | None = None,
        border_width: int | None = None,
        border_spacing: int = 2,
        bg_color: str | Tuple[str, str] = "transparent",
        fg_color: str | Tuple[str, str] | None = None,
        hover_color: str | Tuple[str, str] | None = None,
        border_color: str | Tuple[str, str] | None = None,
        text_color: str | Tuple[str, str] | None = None,
        text_color_disabled: str | Tuple[str, str] | None = None,
        background_corner_colors: Tuple[str | Tuple[str, str]] | None = None,
        round_width_to_even_numbers: bool = True,
        round_height_to_even_numbers: bool = True,
        text: str | Identifier = "CTkButton",
        font: Tuple | CTkFont | None = None,
        textvariable: Variable | None = None,
        image: CTkImage | Any | None = None,
        state: str = "normal",
        hover: bool = True,
        command: Callable[[], Any] | None = None,
        compound: str = "left",
        anchor: str = "center",
        **kwargs
    ):
        super().__init__(
            master,
            width,
            height,
            corner_radius,
            border_width,
            border_spacing,
            bg_color,
            fg_color,
            hover_color,
            border_color,
            text_color,
            text_color_disabled,
            background_corner_colors,
            round_width_to_even_numbers,
            round_height_to_even_numbers,
            _stringify(text,self),
            font,
            textvariable,
            image,
            state,
            hover,
            command,
            compound,
            anchor,
            **kwargs
        )
        self.reg(True, text)

    def create(self, with_master):
        return super().__init__(with_master)


class CheckBox(CTkCheckBox, Widget):
    def __init__(
        self,
        master: Any = None,
        width: int = 100,
        height: int = 24,
        checkbox_width: int = 24,
        checkbox_height: int = 24,
        corner_radius: int | None = None,
        border_width: int | None = None,
        bg_color: str | Tuple[str, str] = "transparent",
        fg_color: str | Tuple[str, str] | None = None,
        hover_color: str | Tuple[str, str] | None = None,
        border_color: str | Tuple[str, str] | None = None,
        checkmark_color: str | Tuple[str, str] | None = None,
        text_color: str | Tuple[str, str] | None = None,
        text_color_disabled: str | Tuple[str, str] | None = None,
        text: str | Identifier = "CTkCheckBox",
        font: Tuple | CTkFont | None = None,
        textvariable: Variable | None = None,
        state: str = tkinter.NORMAL,
        hover: bool = True,
        command: Callable[[], Any] | None = None,
        onvalue: int | str = 1,
        offvalue: int | str = 0,
        variable: Variable | None = None,
        **kwargs
    ):
        super().__init__(
            master,
            width,
            height,
            checkbox_width,
            checkbox_height,
            corner_radius,
            border_width,
            bg_color,
            fg_color,
            hover_color,
            border_color,
            checkmark_color,
            text_color,
            text_color_disabled,
            _stringify(text,self),
            font,
            textvariable,
            state,
            hover,
            command,
            onvalue,
            offvalue,
            variable,
            **kwargs
        )
        self.reg(True, text)

    def create(self, with_master):
        return super().__init__(with_master)


class ComboBox(CTkComboBox, Widget):
    def __init__(
        self,
        master: Any = None,
        width: int = 140,
        height: int = 28,
        corner_radius: int | None = None,
        border_width: int | None = None,
        bg_color: str | Tuple[str, str] = "transparent",
        fg_color: str | Tuple[str, str] | None = None,
        border_color: str | Tuple[str, str] | None = None,
        button_color: str | Tuple[str, str] | None = None,
        button_hover_color: str | Tuple[str, str] | None = None,
        dropdown_fg_color: str | Tuple[str, str] | None = None,
        dropdown_hover_color: str | Tuple[str, str] | None = None,
        dropdown_text_color: str | Tuple[str, str] | None = None,
        text_color: str | Tuple[str, str] | None = None,
        text_color_disabled: str | Tuple[str, str] | None = None,
        font: Tuple | CTkFont | None = None,
        dropdown_font: Tuple | CTkFont | None = None,
        values: List[str] | None = None,
        state: str = tkinter.NORMAL,
        hover: bool = True,
        variable: Variable | None = None,
        command: Callable[[str], Any] | None = None,
        justify: str = "left",
        **kwargs
    ):
        super().__init__(
            master,
            width,
            height,
            corner_radius,
            border_width,
            bg_color,
            fg_color,
            border_color,
            button_color,
            button_hover_color,
            dropdown_fg_color,
            dropdown_hover_color,
            dropdown_text_color,
            text_color,
            text_color_disabled,
            font,
            dropdown_font,
            values,
            state,
            hover,
            variable,
            command,
            justify,
            **kwargs
        )
        self.reg(False)

    def create(self, with_master):
        return super().__init__(with_master)


class Entry(CTkEntry, Widget):
    def __init__(
        self,
        master: Any = None,
        width: int = 140,
        height: int = 28,
        corner_radius: int | None = None,
        border_width: int | None = None,
        bg_color: str | Tuple[str, str] = "transparent",
        fg_color: str | Tuple[str, str] | None = None,
        border_color: str | Tuple[str, str] | None = None,
        text_color: str | Tuple[str, str] | None = None,
        placeholder_text_color: str | Tuple[str, str] | None = None,
        textvariable: Variable | None = None,
        placeholder_text: str | Identifier = "...",
        font: Tuple | CTkFont | None = None,
        state: str = tkinter.NORMAL,
        **kwargs
    ):
        super().__init__(
            master,
            width,
            height,
            corner_radius,
            border_width,
            bg_color,
            fg_color,
            border_color,
            text_color,
            placeholder_text_color,
            textvariable,
            _stringify(placeholder_text,self),
            font,
            state,
            **kwargs
        )
        self.reg(True, placeholder_text, "placeholder_text")

    def create(self, with_master):
        return super().__init__(with_master)


class Frame(CTkFrame, Widget):
    def __init__(
        self,
        master: Any = None,
        width: int = 200,
        height: int = 200,
        corner_radius: int | str | None = None,
        border_width: int | str | None = None,
        bg_color: str | Tuple[str, str] = "transparent",
        fg_color: str | Tuple[str, str] | None = None,
        border_color: str | Tuple[str, str] | None = None,
        background_corner_colors: Tuple[str | Tuple[str, str]] | None = None,
        overwrite_preferred_drawing_method: str | None = None,
        **kwargs
    ):
        super().__init__(
            master,
            width,
            height,
            corner_radius,
            border_width,
            bg_color,
            fg_color,
            border_color,
            background_corner_colors,
            overwrite_preferred_drawing_method,
            **kwargs
        )
        self.reg(False)

    def create(self, with_master):
        return super().__init__(with_master)


class Label(CTkLabel, Widget):
    def __init__(
        self,
        master: Any = None,
        width: int = 0,
        height: int = 28,
        corner_radius: int | None = None,
        bg_color: str | Tuple[str, str] = "transparent",
        fg_color: str | Tuple[str, str] | None = None,
        text_color: str | Tuple[str, str] | None = None,
        text_color_disabled: str | Tuple[str, str] | None = None,
        text: str | Identifier = "CTkLabel",
        font: Tuple | CTkFont | None = None,
        image: CTkImage | None = None,
        compound: str = "center",
        anchor: str = "center",
        wraplength: int = 0,
        **kwargs
    ):
        super().__init__(
            master,
            width,
            height,
            corner_radius,
            bg_color,
            fg_color,
            text_color,
            text_color_disabled,
            _stringify(text,self),
            font,
            image,
            compound,
            anchor,
            wraplength,
            **kwargs
        )
        self.reg(True, text)

    def create(self, with_master):
        return super().__init__(with_master)


class OptionMenu(CTkOptionMenu, Widget):
    def __init__(
        self,
        master: Any = None,
        width: int = 140,
        height: int = 28,
        corner_radius: int | None = None,
        bg_color: str | Tuple[str, str] = "transparent",
        fg_color: str | Tuple[str, str] | None = None,
        button_color: str | Tuple[str, str] | None = None,
        button_hover_color: str | Tuple[str, str] | None = None,
        text_color: str | Tuple[str, str] | None = None,
        text_color_disabled: str | Tuple[str, str] | None = None,
        dropdown_fg_color: str | Tuple[str, str] | None = None,
        dropdown_hover_color: str | Tuple[str, str] | None = None,
        dropdown_text_color: str | Tuple[str, str] | None = None,
        font: Tuple | CTkFont | None = None,
        dropdown_font: Tuple | CTkFont | None = None,
        values: List | None = None,
        variable: Variable | None = None,
        state: str = tkinter.NORMAL,
        hover: bool = True,
        command: Callable[[str | Identifier], Any] | None = None,
        dynamic_resizing: bool = True,
        anchor: str = "w",
        **kwargs
    ):
        super().__init__(
            master,
            width,
            height,
            corner_radius,
            bg_color,
            fg_color,
            button_color,
            button_hover_color,
            text_color,
            text_color_disabled,
            dropdown_fg_color,
            dropdown_hover_color,
            dropdown_text_color,
            font,
            dropdown_font,
            values,
            variable,
            state,
            hover,
            command,
            dynamic_resizing,
            anchor,
            **kwargs
        )
        self.reg(True, values, "values")

    def create(self, with_master):
        return super().__init__(with_master)


class ProgressBar(CTkProgressBar, Widget):
    def __init__(
        self,
        master: Any = None,
        width: int | None = None,
        height: int | None = None,
        corner_radius: int | None = None,
        border_width: int | None = None,
        bg_color: str | Tuple[str, str] = "transparent",
        fg_color: str | Tuple[str, str] | None = None,
        border_color: str | Tuple[str, str] | None = None,
        progress_color: str | Tuple[str, str] | None = None,
        variable: Variable | None = None,
        orientation: str = "horizontal",
        mode: Literal["determinate"] | Literal["indeterminate"] = "determinate",
        determinate_speed: float = 1,
        indeterminate_speed: float = 1,
        **kwargs
    ):
        super().__init__(
            master,
            width,
            height,
            corner_radius,
            border_width,
            bg_color,
            fg_color,
            border_color,
            progress_color,
            variable,
            orientation,
            mode,
            determinate_speed,
            indeterminate_speed,
            **kwargs
        )
        self.reg(False)

    def create(self, with_master):
        return super().__init__(with_master)


class RadioButton(CTkRadioButton, Widget):
    def __init__(
        self,
        master: Any = None,
        width: int = 100,
        height: int = 22,
        radiobutton_width: int = 22,
        radiobutton_height: int = 22,
        corner_radius: int | None = None,
        border_width_unchecked: int | None = None,
        border_width_checked: int | None = None,
        bg_color: str | Tuple[str, str] = "transparent",
        fg_color: str | Tuple[str, str] | None = None,
        hover_color: str | Tuple[str, str] | None = None,
        border_color: str | Tuple[str, str] | None = None,
        text_color: str | Tuple[str, str] | None = None,
        text_color_disabled: str | Tuple[str, str] | None = None,
        text: str | Identifier = "CTkRadioButton",
        font: Tuple | CTkFont | None = None,
        textvariable: Variable | None = None,
        variable: Variable | None = None,
        value: int | str = 0,
        state: str = tkinter.NORMAL,
        hover: bool = True,
        command: Callable[..., Any] | Any = None,
        **kwargs
    ):
        super().__init__(
            master,
            width,
            height,
            radiobutton_width,
            radiobutton_height,
            corner_radius,
            border_width_unchecked,
            border_width_checked,
            bg_color,
            fg_color,
            hover_color,
            border_color,
            text_color,
            text_color_disabled,
            _stringify(text,self),
            font,
            textvariable,
            variable,
            value,
            state,
            hover,
            command,
            **kwargs
        )
        self.reg(True, text)

    def create(self, with_master):
        return super().__init__(with_master)


class Scrollbar(CTkScrollbar, Widget):
    def __init__(
        self,
        master: Any = None,
        width: int | str | None = None,
        height: int | str | None = None,
        corner_radius: int | None = None,
        border_spacing: int | None = None,
        minimum_pixel_length: int = 20,
        bg_color: str | Tuple[str, str] = "transparent",
        fg_color: str | Tuple[str, str] | None = None,
        button_color: str | Tuple[str, str] | None = None,
        button_hover_color: str | Tuple[str, str] | None = None,
        hover: bool = True,
        command: Callable[..., Any] | Any = None,
        orientation: str = "vertical",
        **kwargs
    ):
        super().__init__(
            master,
            width,
            height,
            corner_radius,
            border_spacing,
            minimum_pixel_length,
            bg_color,
            fg_color,
            button_color,
            button_hover_color,
            hover,
            command,
            orientation,
            **kwargs
        )
        self.reg(False)

    def create(self, with_master):
        return super().__init__(with_master)


class SegmentedButton(CTkSegmentedButton, Widget):
    def __init__(
        self,
        master: Any = None,
        width: int = 140,
        height: int = 28,
        corner_radius: int | None = None,
        border_width: int = 3,
        bg_color: str | Tuple[str, str] = "transparent",
        fg_color: str | Tuple[str, str] | None = None,
        selected_color: str | Tuple[str, str] | None = None,
        selected_hover_color: str | Tuple[str, str] | None = None,
        unselected_color: str | Tuple[str, str] | None = None,
        unselected_hover_color: str | Tuple[str, str] | None = None,
        text_color: str | Tuple[str, str] | None = None,
        text_color_disabled: str | Tuple[str, str] | None = None,
        background_corner_colors: Tuple[str | Tuple[str, str]] | None = None,
        font: Tuple | CTkFont | None = None,
        values: List | None = None,
        variable: Variable | None = None,
        dynamic_resizing: bool = True,
        command: Callable[[str], Any] | None = None,
        state: str = "normal",
    ):
        super().__init__(
            master,
            width,
            height,
            corner_radius,
            border_width,
            bg_color,
            fg_color,
            selected_color,
            selected_hover_color,
            unselected_color,
            unselected_hover_color,
            text_color,
            text_color_disabled,
            background_corner_colors,
            font,
            values,
            variable,
            dynamic_resizing,
            command,
            state,
        )
        self.reg(True, values, "values")

    def create(self, with_master):
        return super().__init__(with_master)


class Slider(CTkSlider, Widget):
    def __init__(
        self,
        master: Any = None,
        width: int | None = None,
        height: int | None = None,
        corner_radius: int | None = None,
        button_corner_radius: int | None = None,
        border_width: int | None = None,
        button_length: int | None = None,
        bg_color: str | Tuple[str, str] = "transparent",
        fg_color: str | Tuple[str, str] | None = None,
        border_color: str | Tuple[str, str] = "transparent",
        progress_color: str | Tuple[str, str] | None = None,
        button_color: str | Tuple[str, str] | None = None,
        button_hover_color: str | Tuple[str, str] | None = None,
        from_: int = 0,
        to: int = 1,
        state: str = "normal",
        number_of_steps: int | None = None,
        hover: bool = True,
        command: Callable[[float], Any] | None = None,
        variable: Variable | None = None,
        orientation: str = "horizontal",
        **kwargs
    ):
        super().__init__(
            master,
            width,
            height,
            corner_radius,
            button_corner_radius,
            border_width,
            button_length,
            bg_color,
            fg_color,
            border_color,
            progress_color,
            button_color,
            button_hover_color,
            from_,
            to,
            state,
            number_of_steps,
            hover,
            command,
            variable,
            orientation,
            **kwargs
        )
        self.reg(False)

    def create(self, with_master):
        return super().__init__(with_master)


class Switch(CTkSwitch, Widget):
    def __init__(
        self,
        master: Any = None,
        width: int = 100,
        height: int = 24,
        switch_width: int = 36,
        switch_height: int = 18,
        corner_radius: int | None = None,
        border_width: int | None = None,
        button_length: int | None = None,
        bg_color: str | Tuple[str, str] = "transparent",
        fg_color: str | Tuple[str, str] | None = None,
        border_color: str | Tuple[str, str] = "transparent",
        progress_color: str | Tuple[str, str] | None = None,
        button_color: str | Tuple[str, str] | None = None,
        button_hover_color: str | Tuple[str, str] | None = None,
        text_color: str | Tuple[str, str] | None = None,
        text_color_disabled: str | Tuple[str, str] | None = None,
        text: str | Identifier = "CTkSwitch",
        font: Tuple | CTkFont | None = None,
        textvariable: Variable | None = None,
        onvalue: int | str = 1,
        offvalue: int | str = 0,
        variable: Variable | None = None,
        hover: bool = True,
        command: Callable[..., Any] | Any = None,
        state: str = tkinter.NORMAL,
        **kwargs
    ):
        super().__init__(
            master,
            width,
            height,
            switch_width,
            switch_height,
            corner_radius,
            border_width,
            button_length,
            bg_color,
            fg_color,
            border_color,
            progress_color,
            button_color,
            button_hover_color,
            text_color,
            text_color_disabled,
            _stringify(text,self),
            font,
            textvariable,
            onvalue,
            offvalue,
            variable,
            hover,
            command,
            state,
            **kwargs
        )
        self.reg(True, text)

    def create(self, with_master):
        return super().__init__(with_master)


class Tabview(CTkTabview, Widget):
    def __init__(
        self,
        master: Any = None,
        width: int = 300,
        height: int = 250,
        corner_radius: int | None = None,
        border_width: int | None = None,
        bg_color: str | Tuple[str, str] = "transparent",
        fg_color: str | Tuple[str, str] | None = None,
        border_color: str | Tuple[str, str] | None = None,
        segmented_button_fg_color: str | Tuple[str, str] | None = None,
        segmented_button_selected_color: str | Tuple[str, str] | None = None,
        segmented_button_selected_hover_color: str | Tuple[str, str] | None = None,
        segmented_button_unselected_color: str | Tuple[str, str] | None = None,
        segmented_button_unselected_hover_color: str | Tuple[str, str] | None = None,
        text_color: str | Tuple[str, str] | None = None,
        text_color_disabled: str | Tuple[str, str] | None = None,
        command: Callable[..., Any] | Any = None,
        anchor: str = "center",
        state: str = "normal",
        **kwargs
    ):
        super().__init__(
            master,
            width,
            height,
            corner_radius,
            border_width,
            bg_color,
            fg_color,
            border_color,
            segmented_button_fg_color,
            segmented_button_selected_color,
            segmented_button_selected_hover_color,
            segmented_button_unselected_color,
            segmented_button_unselected_hover_color,
            text_color,
            text_color_disabled,
            command,
            anchor,
            state,
            **kwargs
        )
        self.reg(False)

    def create(self, with_master):
        return super().__init__(with_master)


class Textbox(CTkTextbox, Widget):
    def __init__(
        self,
        master: Any = None,
        width: int = 200,
        height: int = 200,
        corner_radius: int | None = None,
        border_width: int | None = None,
        border_spacing: int = 3,
        bg_color: str | Tuple[str, str] = "transparent",
        fg_color: str | Tuple[str, str] | None = None,
        border_color: str | Tuple[str, str] | None = None,
        text_color: str | None = None,
        scrollbar_button_color: str | Tuple[str, str] | None = None,
        scrollbar_button_hover_color: str | Tuple[str, str] | None = None,
        font: Tuple | CTkFont | None = None,
        activate_scrollbars: bool = True,
        **kwargs
    ):
        super().__init__(
            master,
            width,
            height,
            corner_radius,
            border_width,
            border_spacing,
            bg_color,
            fg_color,
            border_color,
            text_color,
            scrollbar_button_color,
            scrollbar_button_hover_color,
            font,
            activate_scrollbars,
            **kwargs
        )
        self.reg(False)

    def create(self, with_master):
        return super().__init__(with_master)


class ScrollableFrame(CTkScrollableFrame, Widget):
    def __init__(
        self,
        master: Any = None,
        width: int = 200,
        height: int = 200,
        corner_radius: int | str | None = None,
        border_width: int | str | None = None,
        bg_color: str | Tuple[str, str] = "transparent",
        fg_color: str | Tuple[str, str] | None = None,
        border_color: str | Tuple[str, str] | None = None,
        scrollbar_fg_color: str | Tuple[str, str] | None = None,
        scrollbar_button_color: str | Tuple[str, str] | None = None,
        scrollbar_button_hover_color: str | Tuple[str, str] | None = None,
        label_fg_color: str | Tuple[str, str] | None = None,
        label_text_color: str | Tuple[str, str] | None = None,
        label_text: str | Identifier = "",
        label_font: Tuple | CTkFont | None = None,
        label_anchor: str = "center",
        orientation: Literal["vertical"] | Literal["horizontal"] = "vertical",
    ):
        super().__init__(
            master,
            width,
            height,
            corner_radius,
            border_width,
            bg_color,
            fg_color,
            border_color,
            scrollbar_fg_color,
            scrollbar_button_color,
            scrollbar_button_hover_color,
            label_fg_color,
            label_text_color,
            _stringify(label_text,self),
            label_font,
            label_anchor,
            orientation,
        )
        self.reg(False)

    def create(self, with_master):
        return super().__init__(with_master)


class GIF(CTkGIF, Widget):
    def __init__(
        self,
        master=None,
        source: str | bytes | Image | None = None,
        *,
        size: Tuple[int, int] | None = None,
        preserve_aspect: bool = True,
        play_on_start: bool = True,
        start_paused: bool = False,
        loop: bool = True,
        max_loops: int | None = None,
        speed: float = 1,
        fallback_image: str | Image | None = None,
        light_variant: str | bytes | Image | None = None,
        dark_variant: str | bytes | Image | None = None,
        anchor: str = "center",
        **kwargs
    ):
        super().__init__(
            master,
            source,
            size=size,
            preserve_aspect=preserve_aspect,
            play_on_start=play_on_start,
            start_paused=start_paused,
            loop=loop,
            max_loops=max_loops,
            speed=speed,
            fallback_image=fallback_image,
            light_variant=light_variant,
            dark_variant=dark_variant,
            anchor=anchor,
            **kwargs
        )
        self.reg(False)

    def create(self, with_master):
        return super().__init__(with_master)


## == == Special == == ##


class Link(Label):
    def __init__(
        self,
        master: Any = None,
        width: int = 0,
        height: int = 28,
        corner_radius: int | None = None,
        bg_color: str | Tuple[str, str] = "transparent",
        fg_color: str | Tuple[str, str] | None = None,
        text_color: str | Tuple[str, str] | None = None,
        text_color_disabled: str | Tuple[str, str] | None = None,
        text: str | Identifier = "CTkLabel",
        font: Tuple | CTkFont | None = None,
        image: CTkImage | None = None,
        compound: str = "center",
        anchor: str = "center",
        wraplength: int = 0,
        command: Callable | None = None,
        **kwargs
    ):
        super().__init__(
            master,
            width,
            height,
            corner_radius,
            bg_color,
            fg_color,
            text_color,
            text_color_disabled,
            text,
            font,
            image,
            compound,
            anchor,
            wraplength,
            **kwargs
        )
        if command:
            self.bind("<Button1>", command)
