#######################################################################################################################
## Title: Digital photo frame application
## Autor: Jonas dos Santos Silva
## Date: 09/2021
## Release notes: Implemented Fullscreen image feature
##                Added full screen toggle comamand to image button
##                
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

img_settingsbutton_location = "Images/Settings_Icon.jpeg"
img_picturesbutton_location = "Images/pics_icon.png"
img_exitbutton_location = "Images/exit_icon.png"
img_locationbutton_location = "Images/location_icon_1.png"
image_backbutton_location = 'Images/right_transparent_arrow.png'
image_forwardbutton_location = 'Images/right_transparent_arrow.png'

button_subsample_factor = 8
vertical_menu_offset = 30

############################### Definitions - Functions #################################################################

def resizeimage_to_fit(image, fit_width, fit_height): # Resize image to fit a rectangle fit_width x fit_height
    global win_width, win_height 
    image_width, image_height = image.size # Get image dimentions

    w_ratio = fit_width / image_width # Calculate width ration between input width and image
    h_ratio = fit_height / image_height # Calculate height ration between input height and image

    if h_ratio < w_ratio: w_ratio = h_ratio # Set up smallest ratio
    elif w_ratio < h_ratio: h_ratio = w_ratio # Set up smallest ratio
    
    return ImageTk.PhotoImage(image.resize((int(image_width*w_ratio), int(image_height*h_ratio)), Image.ANTIALIAS)) # Resize Image


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
    global current_screen, backbutton, fullscreenbutton, exitbutton, menubutton, forwardbutton, curr_image_button
    curr_image_button.destroy()
    if current_screen == 1: # 1 Image menu
        backbutton.destroy()
        fullscreenbutton.destroy()
        exitbutton.destroy()
        menubutton.destroy()
        forwardbutton.destroy()
        current_screen = 2
    elif current_screen == 2: # 2 Image full screen
        current_screen = 1
        pic_menu_put()
    
    image_put()


def image_put():
    global root, img_index, image_list, vertical_menu_offset, list_len
    global win_width, win_height, curr_image_button, current_screen, curr_image

    if current_screen == 1: # 1 Image menu
        curr_image = resizeimage_to_fit(Image.open(image_list[img_index]), root.winfo_screenwidth(), (root.winfo_screenheight() - vertical_menu_offset))
    elif current_screen == 2: # 2 Image full screen
        curr_image = resizeimage_to_fit(Image.open(image_list[img_index]), root.winfo_screenwidth(), root.winfo_screenheight())
    else: return 1
    
    curr_image_button = Button(root, image=curr_image, command=fullscreen_toggle, cursor='hand2')
    curr_image_button.grid(row=0, columnspan=5, sticky="ew")


def pic_menu_put():
    global root, vertical_menu_offset, backbutton, fullscreenbutton, exitbutton, menubutton, forwardbutton
    #image_forwardbutton = PhotoImage(file=image_forwardbutton_location).subsample(button_subsample_factor, button_subsample_factor)
    #image_backbutton = PhotoImage(file=image_backbutton_location).subsample(button_subsample_factor, button_subsample_factor)

    #backbutton = Button(root, image=image_backbutton, command=thing2, borderwidth=0, cursor='hand2')
    backbutton = Button(root, text = "<< Back", command=back, cursor='hand2')
    fullscreenbutton = Button(root, text = "Full Screen", command=fullscreen_toggle, cursor='hand2')
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


def pictures_menu():
    global current_screen, list_mainmenu_buttons
    current_screen = 1
    index = 0
    for index in range (0, len(list_mainmenu_buttons)):
        list_mainmenu_buttons[index].destroy()
        
    image_put() # Put first image onto window
    pic_menu_put() # Put the first tiem the menu onto window
    
    
def load_mainmenu_images():
    global list_mainmenu_imgs_locations, win_width, win_height
    global img_settingsbutton, img_locationbutton, img_picturesbutton, img_exitbutton
    
    img_settingsbutton = resizeimage_to_fit(Image.open(list_mainmenu_imgs_locations[0]), (root.winfo_screenwidth()/2) , (root.winfo_screenheight()/2) )
    img_locationbutton = resizeimage_to_fit(Image.open(list_mainmenu_imgs_locations[1]), (root.winfo_screenwidth()/2) , (root.winfo_screenheight()/2) )   
    img_picturesbutton = resizeimage_to_fit(Image.open(list_mainmenu_imgs_locations[2]), (root.winfo_screenwidth()/2) , (root.winfo_screenheight()/2) )
    img_exitbutton = resizeimage_to_fit(Image.open(list_mainmenu_imgs_locations[3]), (root.winfo_screenwidth()/2) , (root.winfo_screenheight()/2) )   
       
def main_menu():
    global root, list_mainmenu_imgs_locations, list_mainmenu_buttons
    
    Grid.rowconfigure(root, index=0, weight=1) # index is the row number
    Grid.columnconfigure(root, index=0, weight=1)
    Grid.rowconfigure(root, index=1, weight=1) # index is the row number
    Grid.columnconfigure(root, index=1, weight=1)

    picturesbutton = Button(root, image=img_picturesbutton, command=pictures_menu, cursor='hand2')
    locationbutton = Button(root, image=img_locationbutton, command=root.destroy, cursor='hand2')
    settingsbutton = Button(root, image=img_settingsbutton, command=root.destroy, cursor='hand2')
    exitbutton = Button(root, image=img_exitbutton, command=root.destroy, cursor='hand2')

    picturesbutton.grid(row=0, column=0, sticky="ew")
    locationbutton.grid(row=0, column=1, sticky="ew")
    settingsbutton.grid(row=1, column=0, sticky="ew")
    exitbutton.grid(row=1, column=1, sticky="ew")

    list_mainmenu_buttons = [picturesbutton, locationbutton, settingsbutton, exitbutton]


def main():
    global current_screen
    if current_screen == 0: # 0 Main menu , 1 Image menu, 2 Image full screen, 3 My location, 4 Settings
        main_menu()
    elif current_screen == 1:
        image_put() # Put first image onto window
        pic_menu_put() # Put the first tiem the menu onto window
    # Main Loop
    root.mainloop()

############################### Definitions - Global Variables #######################################################
list_mainmenu_imgs_locations = [img_settingsbutton_location, img_locationbutton_location, img_picturesbutton_location, img_exitbutton_location]
image_list = [image_1_location, image_2_location, image_3_location] # Set up a list of image locations
img_index = 0
list_len = len(image_list)
current_screen = 0 # 0 Main menu , 1 Image menu, 2 Image full screen, 3 My location, 4 Settings
#last_screen = 0 # 0 Main menu , 1 Image menu, 2 Image full screen, 3 My location, 4 Settings
win_width = root.winfo_screenwidth()
win_height = root.winfo_screenheight()

############################### Main Condition/Loop ##################################################################
if __name__ == "__main__":
    try:
        load_mainmenu_images()
        while True:
            main()
    except:
        root.destroy
    finally:
#        ser.close()
#        f.close()
        print('Program Closed')
