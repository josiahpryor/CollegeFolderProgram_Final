import customtkinter as ctk

class homeClassFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        #add widgets to frame
        self.classLb = ctk.CTkLabel(self)
        

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("College Application")
        self.geometry("600x400")

        #grid system
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure((0,1), weight=1)

        #class frame
        self.class_frame = homeClassFrame(master=self)
        self.class_frame.grid(row=0,column=0,padx=20,pady=20,sticky="nesw")

app = App()
app.mainloop()

