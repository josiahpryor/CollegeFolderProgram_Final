import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import shutil
from webLoginAndScrape import collect_classes

#Program to collect college classes from brightspace, create class folders, and sort files into them
class ClassManagementApp:
    def __init__(self, root):
        #base setup
        self.root = root
        self.root.title("Class Management Tool")
        self.root.geometry("900x600")
        #global variables for cross class access
        self.class_list = {}
        self.root_folder_path = ""
        self.files_folder_path = ""
        
        # Setup Frames
        self.setup_frames()
        
        # Initialize UI Components
        self.setup_widgets()

    def setup_frames(self):
        # Overall frame
        self.top_frame = tk.Frame(self.root, padx=10, pady=10)
        self.top_frame.grid(row=0, column=0, columnspan=2, sticky="ew")

        # Left frame - Class fetch and folder creation
        self.class_frame = tk.LabelFrame(self.root, text="Classes", padx=10, pady=10)
        self.class_frame.grid(row=1, column=0, sticky="nesw", padx=10, pady=10)

        # Right frame - File sorting
        self.file_frame = tk.LabelFrame(self.root, text="Files", padx=10, pady=10)
        self.file_frame.grid(row=1, column=1, sticky="nesw", padx=10, pady=10)

    def setup_widgets(self):
        # Classes frame (left frame) widgets
        self.classLB = tk.Listbox(self.class_frame, height=15, width=40)
        self.classLB.pack(fill="both", expand=True, padx=5, pady=5)

        self.fetch_btn = tk.Button(self.class_frame, text="Fetch Classes", command=self.fetch_classes, height=2, width=20)
        self.fetch_btn.pack(pady=5)

        self.folder_btn = tk.Button(self.class_frame, text="Create Folders", command=self.create_folders, height=2, width=20)
        self.folder_btn.pack(pady=5)

        # Files frame (right frame) widgets
        self.parent_folder_CB = ttk.Combobox(self.file_frame, state="readonly", width=50)
        self.parent_folder_CB.pack(pady=5)
        self.parent_folder_CB.set("Select a parent folder (Create folders first)")

        self.class_folder_CB = ttk.Combobox(self.file_frame, state="readonly", width=50)
        self.class_folder_CB.pack(pady=5)
        self.class_folder_CB.set("Select a class folder")

        self.files_LB = tk.Listbox(self.file_frame, selectmode="multiple", height=15, width=40)
        self.files_LB.pack(fill="both", expand=True, padx=5, pady=5)

        self.find_btn = tk.Button(self.file_frame, text="Find Files", command=self.find_files, height=2, width=20)
        self.find_btn.pack(pady=5)

        self.add_btn = tk.Button(self.file_frame, text="Add Files", command=self.add_files, height=2, width=20)
        self.add_btn.pack(pady=5)

        # Configure column and row weights for responsiveness
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

    # Method to fetch classes
    def fetch_classes(self):
        self.class_list = collect_classes()  # Function from webLoginAndScrape.py
        self.classLB.delete(0, tk.END)  # Clear the current class list box
        for class_name in self.class_list:
            self.classLB.insert(tk.END, class_name)  # Add each class to the Listbox

    # Method to create folders
    def create_folders(self):
        if self.class_list: # Ensures classes imported
            self.root_folder_path = filedialog.askdirectory()
            base_folders = ["Documents", "Code"] # Base folders to hold classes
            if self.root_folder_path:
                for folder in base_folders:
                    # Create base folders
                    base_folder_path = os.path.join(self.root_folder_path, folder)
                    os.makedirs(base_folder_path, exist_ok=True)
                    # Create class folders in base folders
                    for class_name in self.class_list:
                        class_folder_path = os.path.join(base_folder_path, class_name)
                        os.makedirs(class_folder_path, exist_ok=True)
                    # Create Previous folder for old classes
                    previous_folder_path = os.path.join(base_folder_path, "[1] Previous")
                    os.makedirs(previous_folder_path, exist_ok=True)

                # Update comboboxes with base and class folders
                self.class_folder_CB['values'] = list(self.class_list)
                self.parent_folder_CB['values'] = base_folders
        else:
            # Must import classes before creating folders
            messagebox.showerror("Error", "Please import classes first")

    # Method to find files for sorting
    def find_files(self):
        # Global file path
        self.files_folder_path = filedialog.askdirectory()
        if self.files_folder_path:
            self.files_LB.delete(0, tk.END)  # Clear the ListBox
            files = os.listdir(self.files_folder_path) # Get file names
            for file in files: 
                self.files_LB.insert(tk.END, file) # Add file names to ListBox

    # Method to add files to selected folder
    def add_files(self):
        selected_files_index = self.files_LB.curselection() # Collects selected files
        selected_files = []
        # Collects folder selection
        class_folder_selected = self.class_folder_CB.get()
        parent_folder_selected = self.parent_folder_CB.get()

        # Add files
        if selected_files_index and class_folder_selected != "Select a class folder" and parent_folder_selected != "Select a parent folder (Create folders first)": # Ensures that all options are selected 
            for index in reversed(selected_files_index): # Reverse to negate index issues
                selected_file = self.files_LB.get(index)
                selected_files.append(selected_file)
                self.files_LB.delete(index)
                # Gather dirs for moving files
                old_folder_path = os.path.join(self.files_folder_path, selected_file)
                new_folder_path = os.path.join(self.root_folder_path, parent_folder_selected, class_folder_selected)
                shutil.move(old_folder_path, new_folder_path)  # Move files

        else: # Error handling
            messagebox.showerror("Error", "Please select files and folders properly.")

# Call main
if __name__ == "__main__":
    root = tk.Tk()
    app = ClassManagementApp(root)
    root.mainloop()
