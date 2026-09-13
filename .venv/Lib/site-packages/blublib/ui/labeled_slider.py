from typing import Any, Tuple, Callable

from .widgets import Frame, Label, Slider, identifier, _stringify, Identifier
from customtkinter import CTkFont, CTkImage, Variable

class LabeledSlider(Frame):
    def __init__(
        self,
        master: Any = None,
        slider_width:int = 200,
        height:int = 50,
        text:str|Identifier = "LCLabeledSlider",
        font: CTkFont | None = None,
        image: CTkImage | None = None,
        from_: int = 0,
        to: int = 1,
        number_of_steps: int | None = None,
        state:str="normal",
        command: Callable[[float],Any] | None = None,
        variable: Variable | None = None
    ):
        super().__init__(
            master,
            fg_color=master.cget("fg_color")
        )

        self.label = Label(
            self,
            0,
            height,
            text=text,
            font=font,
            state=state,
        ).pack(side="left",padx=(0,2))

        self.slider = Slider(
            self,
            slider_width,
            from_=from_,
            to=to,
            number_of_steps=number_of_steps,
            state=state,
            command=command,
            variable=variable
        ).pack(side="left",padx=(2,0))

        if image:
            self.image = Label(
                self,
                state=state,
                text="",
                image=image
            ).pack(side="left",padx=(4,0)).is_literal(True)

    def configure(self, require_redraw=False, **kwargs):
        
        return super().configure(require_redraw, **kwargs)