import customtkinter as ctk

class HomePage(ctk.CTkFrame):
    def __init__(self , parent):
        super().__init__(parent)
        
        self.label = ctk.CTkLabel(self  , text="Home page" , font=ctk.CTkFont(size=24 , weight="bold"))
        self.label.pack(pady=40)