import customtkinter as ctk

class Page(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=0, bg_color=master._bg_color, fg_color=master._fg_color)
    
    def place(self, **kwargs):
        return super().place(anchor="center",relx=0.5,rely=0.5,relwidth=0.98,relheight=0.98, **kwargs)
    