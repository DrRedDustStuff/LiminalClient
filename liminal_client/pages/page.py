from typing import Callable
from ..ui.widgets import ScrollableFrame, Frame

add_page: Callable

pages:"list[type[Page]]" = []
class Page(ScrollableFrame):
    key = "..."
    def __init__(self, parent):
        super().__init__(
            parent,
            corner_radius=0,
            fg_color=parent.cget("fg_color"),
        )
        self.id(self.key)
        self.widgets()
        add_page(self.key,self)

    def show(self):
        self.pack(
            padx=(15, 65),
            pady=(5, 60 - 4),
            fill="both",
            expand=True,
        )

    def hide(self):
        self.pack_forget()

    def widgets(self): ...

    def __init_subclass__(cls) -> None:
        pages.append(cls)