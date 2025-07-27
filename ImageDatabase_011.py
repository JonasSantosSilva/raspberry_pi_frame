#######################################################################################################################
## Title: Digital photo frame application
## Autor: Jonas dos Santos Silva
## Date: 09/2021
## Release notes: Updated resizeimage_to_fit to save instances of menuImg
##                Fixed buttons' size bug of main menu
##                Updated main menu images
##                Implemented auto change image for fullscreen mode
##                
#######################################################################################################################

############################### Imports ##############################################################################
from tkinter import *
from PIL import ImageTk, Image
#from tkinter import filedialog

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

img_settingsbutton_location = "Images/Settings_Icon_6.png"
img_picturesbutton_location = "Images/pics_icon_1.png"
img_exitbutton_location = "Images/exit_icon_3.png"
img_locationbutton_location = "Images/location_icon_1.png" #
image_backbutton_location = 'Images/right_transparent_arrow.png'
image_forwardbutton_location = 'Images/right_transparent_arrow.png'

vertical_menu_offset = 30 # Offset to fit the image menu
current_screen = 0 # 0 Main menu , 1 Image menu, 2 Image full screen, 3 My location, 4 Settings


############################### Definitions - Classes #################################################################
class menuImg:
    def __init__(self, image=None, width=None, height=None, tkindex=None):
        """Constructor Method"""
        self.image = image
        self.width = width
        self.height = height
        self.tkindex = tkindex
    def __str__(self): # STR Method - to print the class
        return f"This is a image used in the menu screens, Width {self.width} Height{self.height}."
    def info(self):
        """This Method return information about the class menuImg."""
        return f"This is a image used in the menu screens, Width {self.width} Height {self.height}."


############################### Definitions - Functions #################################################################

def resizeimage_to_fit(image, fit_width, fit_height, save=False, temp_menuImg=None): # Resize image to fit a rectangle fit_width x fit_height
    global win_width, win_height 
    image_width, image_height = image.size # Get image dimentions

    w_ratio = fit_width / image_width # Calculate width ration between input width and image
    h_ratio = fit_height / image_height # Calculate height ration between input height and image

    if h_ratio < w_ratio: w_ratio = h_ratio # Set up smallest ratio
    elif w_ratio < h_ratio: h_ratio = w_ratio # Set up smallest ratio
    
    resized_img = image.resize((int(image_width*w_ratio), int(image_height*h_ratio)), Image.ANTIALIAS)

    if save:
        temp_menuImg.image = resized_img # Store image
        temp_menuImg.width = int(image_width*w_ratio) # Store image dimentions
        temp_menuImg.height = int(image_height*h_ratio) # Store image dimentions
    
    return ImageTk.PhotoImage(resized_img) # Resize Image


def forward():
    global img_index, list_len
    if img_index == list_len-1: img_index = 0
    else: img_index += 1
    image_put()
        
        
def back():
    global img_index, list_len
    if img_index == 0: img_index = list_len-1
    else: img_index -= 1
    image_put()


def fullscreen_toggle():
    if current_screen == 1: # 1 Image menu
        pic_menu_destroy(2)
    elif current_screen == 2: # 2 Image full screen
        image_destroy(1)

def image_auto_update():
    forward()


def image_destroy(next_screen):
    global current_screen, last_screen
    last_screen = current_screen
    current_screen = next_screen # 0 Main menu , 1 Image menu, 2 Image full screen, 3 My location, 4 Settings
    curr_image_button.destroy()
    main()


def image_put():
    global root, img_index, image_list, vertical_menu_offset, list_len, img_loop
    global win_width, win_height, curr_image_button, current_screen, curr_image

    if current_screen == 1: # 1 Image menu
        curr_image = resizeimage_to_fit(Image.open(image_list[img_index]), root.winfo_screenwidth(), (root.winfo_screenheight() - vertical_menu_offset))
        #if last_screen == 2: curr_image_button.after(cancel)
        if last_screen == 2: root.after_cancel(img_loop)
    elif current_screen == 2: # 2 Image full screen
        curr_image = resizeimage_to_fit(Image.open(image_list[img_index]), root.winfo_screenwidth(), root.winfo_screenheight())
        img_loop = root.after(3000, image_auto_update)
    else: return 1
    
    curr_image_button = Button(root, image=curr_image, command=fullscreen_toggle, cursor='hand2')
    curr_image_button.grid(row=0, columnspan=5, sticky="ew")


def pic_menu_destroy(next_screen): # next_screen -> 0 Main menu , 1 Image menu, 2 Image full screen, 3 My location, 4 Settings
    global list_mainmenu_buttons
    
    all_buttons_list = side_buttons
    all_buttons_list.extend(middle_buttons)
    for button in all_buttons_list:
        button.destroy()
    image_destroy(next_screen)


def pic_menu_put():
    global root, vertical_menu_offset, backbutton, fullscreenbutton, menu_exitbutton, menubutton, forwardbutton, side_buttons, middle_buttons
    #image_forwardbutton = PhotoImage(file=image_forwardbutton_location).subsample(button_subsample_factor, button_subsample_factor)
    #image_backbutton = PhotoImage(file=image_backbutton_location).subsample(button_subsample_factor, button_subsample_factor)

    #backbutton = Button(root, image=image_backbutton, command=thing2, borderwidth=0, cursor='hand2')
    backbutton = Button(root, text = "<< Back", command=back, cursor='hand2')
    fullscreenbutton = Button(root, text = "Full Screen", command=lambda: pic_menu_destroy(2), cursor='hand2')
    menu_exitbutton = Button(root, text = "Exit Program", command=root.destroy, cursor='hand2')
    menubutton = Button(root, text = "Menu", command=lambda: pic_menu_destroy(0), cursor='hand2')
    #forwardbutton = Button(root, image=image_forwardbutton, command=thing1, borderwidth=0, cursor='hand2')
    forwardbutton = Button(root, text = "Forward >>", command=forward, cursor='hand1')

    side_buttons = [backbutton, forwardbutton]
    middle_buttons = [fullscreenbutton, menu_exitbutton, menubutton]

    Grid.rowconfigure(root, index=0, weight=2) # index is the row number
    Grid.columnconfigure(root, index=0, weight=2)
    Grid.columnconfigure(root, index=4, weight=2)
    backbutton.grid(row=1, column=0, sticky="ew", padx=1, pady=1)
    forwardbutton.grid(row=1, column=4, sticky="ew", padx=1, pady=1)
        
    Grid.rowconfigure(root, index=0, weight=1) # index is the row number   
    for index_b, button in enumerate(middle_buttons):
        Grid.columnconfigure(root, index=index_b+1, weight=1)
        button.grid(row=1, column=index_b+1, sticky="ew", padx=1, pady=1)


def pictures_menu():
    global current_screen, list_mainmenu_buttons
    current_screen = 1
       
    image_put() # Put first image onto window
    pic_menu_put() # Put the first tiem the menu onto window
    
    
def load_mainmenu_images():
    global list_mainmenu_imgs_locations, win_width, win_height, menuImg
    global img_settingsbutton_tk, img_locationbutton_tk, img_picturesbutton_tk, img_exitbutton_tk
    global img_settingsbutton, img_locationbutton, img_picturesbutton, img_exitbutton

    img_settingsbutton = menuImg()
    img_locationbutton = menuImg()
    img_picturesbutton = menuImg()
    img_exitbutton = menuImg()

    img_settingsbutton_tk = resizeimage_to_fit(Image.open(list_mainmenu_imgs_locations[0]), (win_width/2), (win_height/2), True, img_settingsbutton)
    img_locationbutton_tk = resizeimage_to_fit(Image.open(list_mainmenu_imgs_locations[1]), (win_width/2), (win_height/2), True, img_locationbutton)   
    img_picturesbutton_tk = resizeimage_to_fit(Image.open(list_mainmenu_imgs_locations[2]), (win_width/2), (win_height/2), True, img_picturesbutton)
    img_exitbutton_tk = resizeimage_to_fit(Image.open(list_mainmenu_imgs_locations[3]), (win_width/2), (win_height/2), True, img_exitbutton)   


def main_menu_destroy(next_screen):
    global list_mainmenu_buttons, current_screen
    current_screen = next_screen # 0 Main menu , 1 Image menu, 2 Image full screen, 3 My location, 4 Settings
    for index in range (0, len(list_mainmenu_buttons)):
        list_mainmenu_buttons[index].destroy()
    main()
    

def main_menu():
    global root, list_mainmenu_imgs_locations, list_mainmenu_buttons
    global img_settingsbutton, img_locationbutton, img_picturesbutton, img_exitbutton
    
    picturesbutton = Button(root, image=img_picturesbutton_tk, command=lambda: main_menu_destroy(1), cursor='hand2')
    locationbutton = Button(root, image=img_locationbutton_tk, command=lambda: main_menu_destroy(3), cursor='hand2')
    settingsbutton = Button(root, image=img_settingsbutton_tk, command=lambda: main_menu_destroy(4), cursor='hand2')
    exitbutton = Button(root, image=img_exitbutton_tk, command=root.destroy, cursor='hand2')

    picturesbutton.grid(row=0, column=0, ipadx=int((win_width/2 - img_picturesbutton.width)/2), ipady=0)
    locationbutton.grid(row=0, column=1, ipadx=int((win_width/2 - img_locationbutton.width)/2), ipady=0)
    settingsbutton.grid(row=1, column=0, ipadx=int((win_width/2 - img_settingsbutton.width)/2), ipady=0)
    exitbutton.grid(row=1, column=1, ipadx=int((win_width/2 - img_exitbutton.width)/2), ipady=0)

    list_mainmenu_buttons = [picturesbutton, locationbutton, settingsbutton, exitbutton]


def main():
    global current_screen
    if current_screen == 0: # 0 Main menu
        main_menu()
    elif current_screen == 1: # 1 Image menu, 2 Image full screen, 3 My location, 4 Settings
        image_put() # Put image onto window
        pic_menu_put() # Put the image menu onto window
    elif current_screen == 2: # 1 Image menu, 2 Image full screen, 3 My location, 4 Settings
        image_put()
    root.mainloop()# Main Loop


def load_files():
    load_mainmenu_images()
    

############################### Definitions - Global Variables #######################################################
list_mainmenu_imgs_locations = [img_settingsbutton_location, img_locationbutton_location, img_picturesbutton_location, img_exitbutton_location]
image_list = [image_1_location, image_2_location, image_3_location] # Set up a list of image locations
img_index = 0
list_len = len(image_list)
last_screen = 0 # 0 Main menu , 1 Image menu, 2 Image full screen, 3 My location, 4 Settings
win_width = root.winfo_screenwidth()
win_height = root.winfo_screenheight()

############################### Main Condition/Loop ##################################################################
if __name__ == "__main__":
    try:
        load_files()
        while True:
            main()
    except:
        root.destroy
    finally:
#        ser.close()
#        f.close()
        print('Program Closed')

