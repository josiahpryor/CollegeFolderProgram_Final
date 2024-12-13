import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from src.CollegeFolderProgram_JosiahP.webLoginAndScrape import *
import os
from tkinter import messagebox
import shutil

#used as global variable
class_list = {}

# Root window
root = tk.Tk()
root.title("Class Managament Tool")
root.geometry("900x600")

#overall frame
top_frame = tk.Frame(root, padx=10,pady=10)
top_frame.grid(row=0,column=0,columnspan=2,sticky="ew")

#left frame - class fetch and folder creation
class_frame = tk.LabelFrame(root,text="Classes",padx=10,pady=10)
class_frame.grid(row=1,column=0,sticky="nesw",padx=10,pady=10)

#right frame - file sort
file_frame = tk.LabelFrame(root, text="Files",padx=10,pady=10)
file_frame.grid(row=1,column=1,sticky="nesw",padx=10,pady=10)



# Function to fetch classes
def fetch_classes():
    global class_list
    class_list = collectClasses() # func from webLoginAndScrape.py
    classLB.delete(0, tk.END)  # Clear the current class list box
    for Class in class_list: 
        classLB.insert(tk.END, Class)  # Add each class to the Listbox
    

def create_folders():
    if class_list: #makes sure classes were imported
        global root_folder_path #used in relocating files
        root_folder_path = filedialog.askdirectory()
        base_folders = ["Documents", "Code"] #expand later? let user choose base folders
        if root_folder_path:
            for folder in base_folders: #makes base folders
                base_folder_path = root_folder_path+f"/{folder}"
                os.makedirs(base_folder_path, exist_ok=True)
                for Class in class_list: #makes class folders in each base folder
                    #expand later? let user choose which classes end up in base folders
                    class_folder_path = base_folder_path+f"/{Class}"
                    os.makedirs(class_folder_path, exist_ok=True)
                    class_folder_path = base_folder_path+f"/[1] Previous" #for old classes
                    os.makedirs(class_folder_path, exist_ok=True)
        #Adds to right frame drop downs once folders created
        class_folder_CB['values'] = list(class_list)
        parent_folder_CB['values'] = base_folders
    else:
        messagebox.showerror("Error", "Please import classes first")
            

def find_files():
    # test_file_sort() - for testing
    global files_folder_path #files to sort
    files_folder_path = filedialog.askdirectory()
    if files_folder_path:
        files_LB.delete(0, tk.END) #clear
        files = os.listdir(files_folder_path) #gathers list of file names
        for file in files: # puts each file name in right frame
            files_LB.insert(tk.END, file)

def test_file_sort(): #test method that just replenishes files for sorting
    #creates files with data that can be sorted
    path = "C:/test"
    os.makedirs(path, exist_ok=True)

    file1 = path+"/file1"
    if not os.path.exists(file1):
        with open(file1, "w") as file:
            file.write("This is test file1")
    file2 = path+"/file2"
    if not os.path.exists(file2):
        with open(file2, "w") as file:
            file.write("This is test file2")
    file3 = path+"/file3"
    if not os.path.exists(file3):
        with open(file3, "w") as file:
            file.write("This is test file3")

def add_files(): #adds files to new dir
    #gets tuple of file indexes in list box
    selected_files_index = files_LB.curselection() 
    selected_files = []
    #gets selected class folder from drop down
    class_folder_selected = class_folder_CB.get()
    #gets selected parent folder from drop down
    parent_folder_selected = parent_folder_CB.get()
    #ensures that user has selected a folder from both drop downs and has imported files
    if selected_files_index and class_folder_selected != class_folder_CB_placeholder and parent_folder_selected != parent_folder_CB_placeholder:
        #reverse to prevent indexing issues when removing
        for index in reversed(selected_files_index):
            selected_file = files_LB.get(index)  # Get the file name at the current index
            selected_files.append(selected_file)  # Add it to the selected files list
            files_LB.delete(index)  # Remove it from the listbox
            #directory concatenation to propely move files
            old_folder_path = files_folder_path+"/"+selected_file
            new_folder_path = root_folder_path+"/"+parent_folder_selected+"/"+class_folder_selected
            shutil.move(old_folder_path, new_folder_path) #move files
    
        
    
    
#Classes frame widgets - left frame
classLB = tk.Listbox(class_frame, height=15, width=40) #display imported classes
classLB.pack(fill="both", expand=True, padx=5,pady=5)

fetch_btn = tk.Button(class_frame, text="Fetch Classes", command=fetch_classes, height=2, width=20)
fetch_btn.pack(pady=5)

folder_btn = tk.Button(class_frame, text="Create Folders", command=create_folders, height=2, width=20)
folder_btn.pack(pady=5)

#Files frame widgets - right frame
parent_folder_paths = []  # List to store available parent_folder destination paths
parent_folder_CB = ttk.Combobox(file_frame, values=parent_folder_paths, state="readonly", width=50)
parent_folder_CB.pack(pady=5)
parent_folder_CB_placeholder = "Select a parent folder (Create folders first)" #important for add_file function
parent_folder_CB.set(parent_folder_CB_placeholder) 

class_folder_paths = []  # List to store available class_folderination paths
class_folder_CB = ttk.Combobox(file_frame, values=class_folder_paths, state="readonly", width=50)
class_folder_CB.pack(pady=5)
class_folder_CB_placeholder = "Select a class folder" #important for add_file function
class_folder_CB.set(class_folder_CB_placeholder) 

files_LB = tk.Listbox(file_frame, selectmode="multiple", height=15, width=40)
files_LB.pack(fill="both", expand=True,padx=5,pady=5)

find_btn = tk.Button(file_frame, text="Find Files", command=find_files, height=2, width=20)
find_btn.pack(pady=5)

add_btn = tk.Button(file_frame, text="Add Files", command=add_files, height=2,width=20 )
add_btn.pack(pady=5)


# Configure column and row weights for responsiveness
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)



root.mainloop()

