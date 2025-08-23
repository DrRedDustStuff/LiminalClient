from tkinter import Text, END
from tkinter import font as tkfont
from typing import Any, Tuple
import customtkinter as ctk

CPOS = "end-1c"

class CTkCreator(ctk.CTkScrollableFrame):
    """
    Creates widgets based on md-ast.
    Note: does not store children for easy access.
    """
    def __init__(self, master: Any, ast: list[dict[str, Any]], width: int = 200, height: int = 200, 
                 corner_radius: int | str | None = None, border_width: int | str | None = None, 
                 bg_color: str | Tuple[str, str] = "transparent", fg_color: str | Tuple[str, str] | None = None, 
                 border_color: str | Tuple[str, str] | None = None,
                 **kwargs):
        super().__init__(master, width=width, height=height, corner_radius=corner_radius, 
                         border_width=border_width, bg_color=bg_color, fg_color=fg_color, 
                         border_color=border_color, **kwargs)

        self.create(self, "root", ast)

    def create(self, parent: Any, parent_type: str, data: list[dict[str, Any]]):
        "Recursively creates widgets based on node type"
        match parent_type:
            case "root":
                self.handle_root(parent, data)

    def handle_root(self, parent: Any, data: list[dict[str, Any]]):
        for node in data:
            match node["type"]:
                case "heading":
                    self.widget_heading(parent, node)
                case "paragraph":
                    self.widget_paragraph(parent, node)
                case "list":
                    self.widget_list(parent, node)
                case "block_code":
                    self.widget_code(parent, node)
                case _:
                    pass  # unhandled types
            #ctk.CTkFrame(self, 2, 5, 50).pack(pady=4, fill="x", anchor="w") # add breaker line, unnecessary as html can do the same thing

    # ----------------------------
    # Widget implementations
    # ----------------------------

    def widget_heading(self, parent: Any, node: dict[str, Any]):
        level = node.get("attrs", {}).get("level", 1)
        font_size = max(24 - (level - 1) * 4, 10)

        # CTkTextbox to allow inline styling inside a heading
        textbox = ctk.CTkTextbox(parent, width=500, height=1, activate_scrollbars=False)
        textbox.pack(anchor="w", padx=0, fill="x")
        tw = textbox._textbox  # underlying tk.Text

        # Make it look like a label
        tw.configure(wrap="word", borderwidth=0, highlightthickness=0, padx=0, pady=0)

        # BASE FONT: set this so the whole heading scales
        tw.configure(font=("Arial", font_size))

        # Inline styles at the same heading size
        tw.tag_configure("bold",   font=("Arial",  font_size, "bold"))
        tw.tag_configure("italic", font=("Arial",  font_size, "italic"))
        #tw.tag_configure("code",   font=("Courier", font_size)) # should not be necessary

        # Insert children with inline styling (expects text in node["raw"])
        for child in node.get("children", []):
            print(child["type"])
            self.insert_inline_text(tw, child, heading=True, font_size=font_size)

        # Read-only
        tw.configure(state="disabled")

        # Resize height to fit content (pixels)
        textbox.update_idletasks()
        line_h = tkfont.Font(font=("Arial", font_size)).metrics("linespace")
        try:
            count = tw.count("1.0", "end-1c", "displaylines")
            lines = count[0] if count else 1
        except Exception:
            # Fallback if 'displaylines' unsupported
            lines = int(tw.index("end-1c").split(".")[0])
        textbox.configure(height=max(line_h * max(1, lines), line_h))

    def widget_paragraph(self, parent: Any, node: dict[str, Any]):
        # Use CTkTextbox to allow inline styling
        textbox = ctk.CTkTextbox(parent, width=500, height=1, activate_scrollbars=False)
        textbox.pack(anchor="w", fill="x")
        tw: Text = textbox._textbox  # underlying Text widget

        font_size = 11

        # Inline styles at the same heading size
        tw.configure(font=("Arial", font_size))
        tw.tag_configure("bold",   font=("Arial",  font_size, "bold"))
        tw.tag_configure("italic", font=("Arial",  font_size, "italic"))
        tw.tag_configure("code",   font=("Courier", font_size), background=self._apply_appearance_mode(["#A7A7A7","#535353"]), selectbackground="#0062B3")
        tw.tag_configure("link",   font=("Arial", font_size), foreground="#0ba3e9", underline=True)

        # Insert children with inline styling (expects text in node["raw"])
        for child in node.get("children", []):
            print(child["type"])
            self.insert_inline_text(tw, child, font_size=font_size)

        # Read-only
        tw.configure(state="disabled")

        # Resize height to fit content (pixels)
        textbox.update_idletasks()
        line_h = tkfont.Font(font=("Arial", font_size)).metrics("linespace")
        try:
            count = tw.count("1.0", CPOS, "displaylines")
            lines = count[0] if count else 1
        except Exception:
            # Fallback if 'displaylines' unsupported
            lines = int(tw.index(END).split(".")[0])
        textbox.configure(height=max(line_h * max(1, lines), line_h))
        print(max(line_h * max(1, lines), line_h))
        print(lines)

    def insert_inline_text(self, text_widget: Text, node: dict[str, Any], heading: bool = False, font_size: int = 12):
        ntype = node["type"]

        if ntype == "text":
            text_widget.insert("end", node.get("raw", ""))
        elif ntype == "strong":
            start = text_widget.index(CPOS)
            for c in node.get("children", []):
                print(c["type"])
                self.insert_inline_text(text_widget, c, heading=heading, font_size=font_size)
            end = text_widget.index(CPOS)
            text_widget.tag_add("bold", start, end)
            print(f"index from {start} to {end}, strong")
        elif ntype == "emphasis":
            start = text_widget.index(CPOS)
            for c in node.get("children", []):
                print(c["type"])
                self.insert_inline_text(text_widget, c, heading=heading, font_size=font_size)
            end = text_widget.index(CPOS)
            text_widget.tag_add("italic", start, end)
            print(f"index from {start} to {end}, emphasis")
        elif ntype == "inline_code":
            start = text_widget.index(CPOS)
            text_widget.insert("end", node.get("raw", ""))
            end = text_widget.index(CPOS)
            text_widget.tag_add("code", start, end)
            print(f"index from {start} to {end}, inline_code")
        elif ntype == "codespan":
            start = text_widget.index(CPOS)
            text_widget.insert("end", node.get("raw", ""))
            end = text_widget.index(CPOS)
            text_widget.tag_add("code", start, end)
            print(f"index from {start} to {end}, codespan")
        elif ntype == "link":
            # render link text; you can also add URL afterwards if you want
            start = text_widget.index(CPOS)
            for c in node.get("children", []):
                print(c["type"])
                self.insert_inline_text(text_widget, c, heading=heading, font_size=font_size)
            end = text_widget.index(CPOS)
            # example styling for links (inherits base size)
            
            text_widget.tag_add("link", start, end)
            print(f"index from {start} to {end}, link")
        elif ntype == "softbreak":
            text_widget.insert("end", "\n")
        print()

    def widget_list(self, parent: Any, node: dict[str, Any], level: int = 0):
        bullet = "• "
        for idx, item in enumerate(node.get("children", []), start=1):
            prefix = f"{idx}. " if node.get("ordered", False) else bullet
            if "children" in item:
                for child in item["children"]:
                    if child["type"] == "paragraph":
                        # Prepend bullet
                        text = (prefix or "") + self.extract_text(child.get("children", []))
                        label = ctk.CTkLabel(parent, text=text, wraplength=480, justify="left")
                        label.pack(anchor="w", padx=level*20, pady=1)
                    elif child["type"] == "list":
                        self.widget_list(parent, child, level+1)

    def widget_code(self, parent: Any, node: dict[str, Any]):
        textbox = ctk.CTkTextbox(parent, width=500, height=100, fg_color="#1e1e1e", text_color="#dcdcaa")
        textbox.pack(anchor="w")
        
        text_widget = textbox._textbox  # underlying Tkinter Text widget
        text_widget.insert("0.0", node.get("raw", ""))
        
        # Set font on the Tk Text widget
        text_widget.configure(font=("Courier", 12))
        
        # Make it read-only
        text_widget.configure(state="disabled")

        
    # ----------------------------
    # Helper
    # ----------------------------
    def extract_text(self, children: list[dict[str, Any | str | list]]) -> str:
        """Recursively extract plain text from inline nodes"""
        text = ""
        for node in children:
            ntype = node["type"]
            if ntype == "text":
                if isinstance(node["raw"], str):
                    text += node["raw"]
                
            elif ntype in ("strong", "emphasis", "inline_code", "link"):
                cl = node.get("children", [])
                if isinstance(cl, list):
                    text += self.extract_text(cl)
        return text
