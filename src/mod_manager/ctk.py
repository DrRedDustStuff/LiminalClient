"""CustomTkinter Integration
<br /><b> *(special case development)</b>"""

from typing import Any
import customtkinter as ctk

from .mod import Mod

# TODO
# Cleanup -low priority
class ModDisplay(ctk.CTkFrame):
    def __init__(self, master: Any, modpage_function, mod:Mod | None = None, width: int = 200, height: int = 200, **kwargs):
        super().__init__(master, width, height, 16, 2, "transparent", "transparent", None, None, None, **kwargs)
        self.modpage_function = modpage_function
        self.mod: Mod | None = None
        if mod: self.mod = mod
        self.create_widgets(self)

    def create_widgets(self, master):
        # use master as the root master. use self.<widget> as sub-master
        # structure like this:
        # master
        # - widget
        # - sub-master
        # -- widget
        # *(nested widgets follow these rules as well)

        # mod select checkbox
        self.cb_select = ctk.CTkCheckBox(self, width=16,height=16, text="")
        self.cb_select.pack(side="left", padx=(12,5),pady=5)

        # mod icon image-label
        self.il_mod_icon = ctk.CTkButton(master, width=64, height=64, text="", image=None)
        if self.mod:
            self.il_mod_icon.configure(False, command=lambda: self.modpage_function("Modpage", False, self.mod))
        self.il_mod_icon.pack(side="left", padx=5,pady=5)

        # mod name/author container
        self.lf_mod_author_name_container = ctk.CTkFrame(master, corner_radius=0, fg_color="transparent")
        self.lf_mod_author_name_container.pack(side="left", padx=5,pady=5)
        # mod name label : mnac
        self.l_mod_name = ctk.CTkLabel(self.lf_mod_author_name_container, text="MODNAME")
        self.l_mod_name.pack(side="top",pady=1)
        # mod author label : mnac
        self.l_mod_author = ctk.CTkLabel(self.lf_mod_author_name_container, text="MODAUTHOR")
        self.l_mod_author.pack(side="bottom",pady=1)
        # mnac :

        # mod version/filename container
        self.lf_mod_version_filename_container = ctk.CTkFrame(master, corner_radius=0, fg_color="transparent")
        self.lf_mod_version_filename_container.pack(padx=5,pady=5)
        # mod version label : mvfc
        self.l_mod_version = ctk.CTkLabel(self.lf_mod_version_filename_container, text="MODVERSION")
        self.l_mod_version.pack(side="top",pady=1)
        # mod filename label : mvfc
        self.l_mod_filename = ctk.CTkLabel(self.lf_mod_version_filename_container, text="MODFILENAME")
        self.l_mod_filename.pack(side="bottom",pady=1)
        # mvfc :

        # more options ...
    
    def set_mod(self, mod:Mod) -> None:
        self.mod = mod
        self.set_values(mod_author=self.mod.author)
    
    def set_values(self, **kwargs):
        # could use translation manager (would not recommend)
        """Valid -> mod_icon, mod_name, mod_author, version, filename"""
        self.l_mod_name    .configure(False, text=kwargs["mod_name"  ]) if kwargs["mod_name"  ] else None
        self.l_mod_author  .configure(False, text=kwargs["mod_author"]) if kwargs["mod_author"] else None
        self.l_mod_version .configure(False, text=kwargs["version"   ]) if kwargs["version"   ] else None
        self.l_mod_filename.configure(False, text=kwargs["filename"  ]) if kwargs["filename"  ] else None