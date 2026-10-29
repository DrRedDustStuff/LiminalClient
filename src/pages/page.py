from typing import Callable
from blublib.ui.widgets import ScrollableFrame, Frame
from blublib.resource import Identifier

add_page: Callable

pages:"list[type[Page]]" = []
class Page(ScrollableFrame):
    plugin: str = "Source"
    key: Identifier = Identifier.get("...","")
    add_direct = True
    def __init__(self, parent) -> None:
        super().__init__(
            parent,
            corner_radius=0,
            fg_color=parent.cget("fg_color"),
        )
        self.id(self.key.getNamespace()+"."+self.key.getPath()+".page")
        self.widgets()

    def __un_init__(self) -> None: ...

    def show(self) -> None:
        self.pack(
            padx=(15, 65),
            pady=(5, 60 - 4),
            fill="both",
            expand=True,
        )

    def hide(self) -> None:
        self.pack_forget()

    def widgets(self) -> None: ...

    def __init_subclass__(cls) -> None:
        pages.append(cls)

    