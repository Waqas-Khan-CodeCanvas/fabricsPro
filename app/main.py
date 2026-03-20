import customtkinter as ctk
from configs import app_config
from pages.Home import HomePage

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("applicatoin")
        self.geometry("1000x600")
        
        self.sidebar = ctk.CTkFrame(self , width=200 , corner_radius=0)
        self.sidebar.pack(side="left" , fill="y")
        
        self.container = ctk.CTkFrame(self,fg_color="grey")
        self.container.pack(side="right" , expand=True , fill="both")
        
        self.home = HomePage(self.container)
        self.home.place(relx=0 , rely=0 , relwidth=1 , relheight=1)
        
        
if __name__ == "__main__":
    app = App()
    app.mainloop()
        
        