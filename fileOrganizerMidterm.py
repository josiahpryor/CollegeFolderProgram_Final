import os

base_dir = "" #Global variable created for methods to access base directory

'''
Method created for formatting console ouput.
Helps organize and keep track of prompting by creating seperation.
'''
def line():
    print("--------------------------------------------")

'''
Simplified method for creating a folder through OS.
Sets exist_ok=True for all paths sent to it.
'''
def makedirs(path):
    os.makedirs(path, exist_ok=True)

'''
Retrieves a working directory from the user.
If directory is not accurate, the loop will ask the 
user to reinput a working directory.
'''
def customDir():
    while True:
            path = input("-> Please enter your desired directory: ")
            if(os.path.isdir(path)):
                return path
            else: print(f"\"{path}\" is not a valid directory")

'''
Simplified method for retrieving the default document directory
of the user. Expanduser("~") locates the user's root directory.
'''
def defaultDir():
    path = os.path.expanduser("~\\Documents\\")
    return path

'''
Used when asking yes or no questions with user input in conjunction with an if/else.
Yes/y = True, no/n = False
'''
def yesORno (prompt="Enter yes or no: "): #default prompt if none provided
    while True: #loops until yes/y or no/no is provided. 
        answer = input(prompt).strip().lower()
        if answer in ("yes", "y"):
            return True
        elif answer in ("no", "n"):
            return False
        else:
            print("Invalid input: Please enter 'yes' or 'no'")

'''
Asks the user for their class amount and then iterates through that amount
collecting their class name and inserting them into a classes list that is returned.
'''
def classCollection():
    classes = [] 
    #Asks for class amount
    while True:
        try:
            classAmount = int(input("-> How many classes do you have?: "))
            line()
            break
        except ValueError:
            print("Please enter a valid number")
    #Asks for class names based on amount
    if classAmount > 0:
        print("<- Please enter class names with the format you name your files ->")
        print("<- Example: \"CIS-123\"")
        for Class in range(classAmount):
            Class += 1
            classes.append(str(input("-> Class name: ")))
        line()
        return classes
    else: #if a negative number of classes is inputted, this is skipped
        pass

'''
Allows user to choose between preset base folder for storing future 
college class subfolders or their own desired directory. 
'''
def createBaseFolder():
    global base_dir #Global var. for other methods to access
    print("<- Base folder example: \\Users\\username\\Documents ->")
    #yes = true, no = false
    if yesORno("-> Would you like your base college folder stored here?: "):
        #collects default or custom path
        path = defaultDir() + "\\College\\"
    else:
        path = customDir() + "\\College\\"
    base_dir = path
    makedirs(base_dir) #makes dir
    
'''
Creates subfolders with class names inside base college folder.
'''
def createSubFolders(classes): #list of class names
    class_dir = ""
    for Class in classes:
        #\user\documents + \className
        class_dir = os.path.join(base_dir, Class) #uses base dir global var. to add class subdirectory
        makedirs(class_dir) #makes folder of base_dir + classname 

'''
Searches each file's name for a match to one of the class names inputted earlier.
Makes:
{Class1: Class1_file1, Class1_file2; Class2: Class2_file1, Class2_file2}

'''
def searchDirectory(directory, classes):
    files = os.listdir(directory) #provides list of all files/folders in directory
    #Creates new list of only files - filters out folders in directory
    file_names = [file for file in files if os.path.isfile(os.path.join(directory, file))]
    fileSearch = {} #Dictionary: key: class name, value: list of files including that class name
    for Class in classes: 
        fileSearch[Class] = [] 
        for file in file_names:
            if Class in file:
                fileSearch[Class].append(file)
    return fileSearch

'''
Moves files from file directory to newly created college class folders based off of the sorted
dictionary provided in searchDirectory().
'''
def moveFiles(files_dir, class_dict):
    global base_dir 
    for Class in class_dict: #for each inputted class
        class_dir = base_dir + Class #creates path for new college class folders
        for files in class_dict[Class]: #Key: Classname, Value: list of files <- accessing
            old_file_dir = files_dir + "\\" + files #Creates path of current file dir.
            new_file_dir = class_dir + "\\" + files #Creates path of where to move file
            os.rename(old_file_dir, new_file_dir) #rename moves file when two paths are provided
    

'''
Allows the user to choose between the default document dir. or their own dir. to
locate files they'd like to sort into new college folder
'''
def sortFiles(classes):
    line()
    print("<- File Sorting: Sort files into your new college class folders ->")
    print("<- Any file that includes one of your provided classes in its name will be sorted into its respective folder ->")
    if yesORno("-> Are your files located in your default document folder?: "):
        files_dir = defaultDir() #\user\documents
    else:
        files_dir = customDir()
    class_dict = searchDirectory(files_dir, classes) #With provided dir., files including a class name are sorted into a dict
    moveFiles(files_dir, class_dict) #files moved from file dir. to class folder dir. based off name
    print("<- Your files have been sorted into your college class folders ->\n")
    
'''
Main method for beginning program and calling methods
'''
def main():

    line()
    print("This program is designed for college students\n"
    "It uses folder creation and file sorting to help student's organization")
    line()

    classes = classCollection()
    if not classes:
        return

    createBaseFolder()

    createSubFolders(classes)

    sortFiles(classes)

main()



