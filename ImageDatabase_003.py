#######################################################################################################################
## Title: Digital photo frame application
## Autor: Jonas dos Santos Silva
## Date: 09/2021
## Release notes: Image resize included
#######################################################################################################################

############################### Imports ##############################################################################
from tkinter import *
from PIL import ImageTk, Image
from tkinter import filedialog

############################### Definitions - Main Window ####################################################################
root = Tk()

############################### Settings ##############################################################################
#root.minsize(900, 900)
#root.geometry("1000x1000")
root.title("## Test ##")
root.attributes('-fullscreen', True)
image_location = "Images/background_example.jpeg"
image_backbutton_location = 'Images/right_transparent_arrow.png'
image_forwardbutton_location = 'Images/right_transparent_arrow.png'
button_subsample_factor = 8

############################### Definitions - Functions #################################################################
def fullscreen():
    return

############################### Image ###################################################################################
#print("Window With ", root.winfo_screenwidth())
#print("Window Heigh ", root.winfo_screenheight())
win_width = root.winfo_screenwidth()
win_height = root.winfo_screenheight()

my_image = Image.open(image_location) # Open Image
resized_image = my_image.resize((win_width, win_height-30), Image.ANTIALIAS) # Resize Image
new_image = ImageTk.PhotoImage(resized_image) # Define the image
Label(root, image=new_image).grid(row=0, columnspan=5, sticky="ew")

###############################  Menu ##################################################################################
image_forwardbutton = PhotoImage(file=image_forwardbutton_location).subsample(button_subsample_factor, button_subsample_factor)
image_backbutton = PhotoImage(file=image_backbutton_location).subsample(button_subsample_factor, button_subsample_factor)

#backbutton = Button(root, image=image_backbutton, command=thing2, borderwidth=0, cursor='hand2')
backbutton = Button(root, text = "Back", command=root.destroy, cursor='hand2')
fullscreenbutton = Button(root, text = "Full Screen", command=fullscreen, cursor='hand2')
exitbutton = Button(root, text = "Exit Program", command=root.destroy, cursor='hand2')
menubutton = Button(root, text = "Menu", command=root.destroy, cursor='hand2')
#forwardbutton = Button(root, image=image_forwardbutton, command=thing1, borderwidth=0, cursor='hand2')
forwardbutton = Button(root, text = "Forward", command=root.destroy, cursor='hand2')

side_buttons = [backbutton, forwardbutton]
middle_buttons = [fullscreenbutton, exitbutton, menubutton]

Grid.rowconfigure(root, index=0, weight=2) # index is the row number
Grid.columnconfigure(root, index=0, weight=2)
Grid.columnconfigure(root, index=4, weight=2)
backbutton.grid(row=1, column=0, sticky="ew", padx=1, pady=1)
forwardbutton.grid(row=1, column=4, sticky="ew", padx=1, pady=1)
    
Grid.rowconfigure(root, index=0, weight=1) # index is the row number   
for index_b, button in enumerate(middle_buttons):
    Grid.columnconfigure(root, index=index_b+1, weight=1)
    button.grid(row=1, column=index_b+1, sticky="ew", padx=1, pady=1)
   

# Main Loop
root.mainloop()