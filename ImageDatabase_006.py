#######################################################################################################################
## Title: Digital photo frame application
## Autor: Jonas dos Santos Silva
## Date: 09/2021
## Release notes: Added list of images
##                Implemented forward and back buttons
##                implemented function to update image
##                implemented function to update menu
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

image_1_location = "Images/jss_icon_test_2.png"
image_2_location = "Images/big_image.jpeg"
image_3_location = "Images/background_example.jpeg"
image_location = "Images/big_image.jpeg"
image_backbutton_location = 'Images/right_transparent_arrow.png'
image_forwardbutton_location = 'Images/right_transparent_arrow.png'

button_subsample_factor = 8
vertical_menu_offset = 30

############################### Definitions - Functions #################################################################
def fullscreen():
    return


def image_update():
    global root, img_index, my_lable, image_list, vertical_menu_offset, list_len, new_image
    
    win_width = root.winfo_screenwidth()
    win_height = root.winfo_screenheight()

    curr_image = Image.open(image_list[img_index]) # Open Image
    image_width, image_height = curr_image.size # Get image dimentions

    w_ratio = root.winfo_screenwidth() / image_width # Calculate width ration between screen and image
    h_ratio = (root.winfo_screenheight() - vertical_menu_offset) / image_height # Calculate height ration between screen and image

    if h_ratio < w_ratio: w_ratio = h_ratio # Set up smallest ratio
    elif w_ratio < h_ratio: h_ratio = w_ratio # Set up smallest ratio
    
    resized_image = curr_image.resize((int(image_width*w_ratio), int(image_height*h_ratio)), Image.ANTIALIAS) # Resize Image
    new_image = ImageTk.PhotoImage(resized_image) # Define the image
    Button(root, image=new_image, command=root.destroy, cursor='hand2').grid(row=0, columnspan=5, sticky="ew")


def menu_update():
    global root, vertical_menu_offset
    image_forwardbutton = PhotoImage(file=image_forwardbutton_location).subsample(button_subsample_factor, button_subsample_factor)
    image_backbutton = PhotoImage(file=image_backbutton_location).subsample(button_subsample_factor, button_subsample_factor)

    #backbutton = Button(root, image=image_backbutton, command=thing2, borderwidth=0, cursor='hand2')
    backbutton = Button(root, text = "<< Back", command=back, cursor='hand2')
    fullscreenbutton = Button(root, text = "Full Screen", command=fullscreen, cursor='hand2')
    exitbutton = Button(root, text = "Exit Program", command=root.destroy, cursor='hand2')
    menubutton = Button(root, text = "Menu", command=root.destroy, cursor='hand2')
    #forwardbutton = Button(root, image=image_forwardbutton, command=thing1, borderwidth=0, cursor='hand2')
    forwardbutton = Button(root, text = "Forward >>", command=forward, cursor='hand1')

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


def forward():
    global img_index, list_len
    #global my_lable
    if img_index == list_len-1: img_index = 0
    else: img_index += 1
    #my_lable.grid_forget()
    image_update()
        
        
def back():
    global img_index, list_len
    #global my_lable
    if img_index == 0: img_index = list_len-1
    else: img_index -= 1
    #my_lable.grid_forget()
    image_update()


# Set up a list of image locations
image_list = [image_1_location, image_2_location, image_3_location]
img_index = 0
list_len = len(image_list)

# Put first image onto window
image_update()

# Put the first tiem the menu onto window
menu_update()

# Main Loop
root.mainloop()
