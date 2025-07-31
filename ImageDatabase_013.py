#######################################################################################################################
## Title: Digital photo frame application
## Autor: Jonas dos Santos Silva
## Date: 09/2021
## Release notes: Removed Fullscreen and Exit buttons from pictutre menu
##                Implemented read config file
##                Implemented write config file
##                Implemented settings menu
##                Implemented "settings_menu_destroy" function
##                
#######################################################################################################################

############################### Imports ##############################################################################
from tkinter import *
from PIL import ImageTk, Image
import GPS_03
#import subprocess
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
img_locationbutton_location = "Images/location_icon_1.png"
image_backbutton_location = 'Images/right_transparent_arrow.png'
image_forwardbutton_location = 'Images/right_transparent_arrow.png'

cmd_py_location = '/home/pi/Documents/Python/Projects/GPS_0.3.py'

vertical_menu_offset = 30 # Offset to fit the image menu
current_screen = 0 # 0 Main menu , 1 Image menu, 2 Image full screen, 3 My location, 4 Settings
pic_change_delay_ms = 3000 # Time bewtween chamging pictures in fullscreen mode | This value might be replaced by the Config file


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
    global img_index, list_len, current_screen
    if img_index == list_len-1: img_index = 0
    else: img_index += 1

    if current_screen == 1: # 1 Image menu
        pic_menu_destroy(1)
    elif current_screen == 2: # 2 Image full screen
        image_destroy(2)


def back():
    global img_index, list_len, current_screen
    if img_index == 0: img_index = list_len-1
    else: img_index -= 1
    
    if current_screen == 1: # 1 Image menu
        pic_menu_destroy(1)
    elif current_screen == 2: # 2 Image full screen
        image_destroy(2)


def fullscreen_toggle():
    if current_screen == 1: # 1 Image menu
        pic_menu_destroy(2)
    elif current_screen == 2: # 2 Image full screen
        image_destroy(1)


def image_auto_update():
    forward()


def call_location_script():
    global current_screen
    current_screen = 0
    GPS_03.main()
    main()
#     global subprocess
#     p = subprocess.Popen(cmd_py_location, shell=True)
#     out, err = p.communicate()
#     print(f"call_location_script() - out {out} err {err}")


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
        img_loop = root.after(pic_change_delay_ms, image_auto_update)
    else: return 1
    
    curr_image_button = Button(root, image=curr_image, command=fullscreen_toggle, cursor='hand2')
    curr_image_button.grid(row=0, columnspan=3, sticky="nsew")


def pic_menu_destroy(next_screen): # next_screen -> 0 Main menu , 1 Image menu, 2 Image full screen, 3 My location, 4 Settings
    global pic_menu_buttons
    
    for button in pic_menu_buttons:
        button.destroy()
    image_destroy(next_screen)


def pic_menu_put():
    global root, vertical_menu_offset, pic_menu_buttons,  backbutton, menubutton, forwardbutton
    
    #image_forwardbutton = PhotoImage(file=image_forwardbutton_location).subsample(button_subsample_factor, button_subsample_factor)
    #image_backbutton = PhotoImage(file=image_backbutton_location).subsample(button_subsample_factor, button_subsample_factor)

    #backbutton = Button(root, image=image_backbutton, command=thing2, borderwidth=0, cursor='hand2')
    backbutton = Button(root, text = "<< Back", command=back, font=("Helvetica", 42), cursor='hand2')
    menubutton = Button(root, text = "Menu", command=lambda: pic_menu_destroy(0), font=("Helvetica", 42), cursor='hand2')
    forwardbutton = Button(root, text = "Forward >>", command=forward, font=("Helvetica", 42), cursor='hand1')

    pic_menu_buttons = [backbutton, menubutton, forwardbutton]

    Grid.rowconfigure(root, index=0, weight=1) # index is the row number
    Grid.rowconfigure(root, index=1, weight=1) # index is the row number
    for index_b, button in enumerate(pic_menu_buttons):
        Grid.columnconfigure(root, index=index_b, weight=1)
        button.grid(row=1, column=index_b, sticky="ew", padx=1, pady=1)


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


def settings_menu_destroy(next_screen):
    global current_screen, list_settings_menu_widgets

    for widget in list_settings_menu_widgets:
        widget.destroy()
    
    current_screen = next_screen
    main()


def settings_menu():
    global list_settings_menu_widgets
    
    radio_input= IntVar() # Declaring Tkinter variable (Not: use "radio_input.get()" to read the variable)
    
    title_pic = Label(root, text="PICTURES", font=("Helvetica", 24))
    title_pic.pack(pady=20)
    title_pic_delay = Label(root, text="Auto change delay:", font=("Helvetica", 16))
    title_pic_delay.pack(pady=10)
    
    delays = [("2s", "2000"),
              ("3s", "3000"),
              ("4s", "4000"),
              ("8s", "4000"),
              ("16s", "8000")]

    delay = StringVar()
    delay.set("3000")
    
#     for text, time_ms in delays: # Declaring Radio Buttons
#         Radiobutton(root, text=text, variable=delay, value=time_ms, font=("Helvetica", 16)).pack(pady=10)
        
    settings_2s = Radiobutton(root, text="2s", variable=delay, value=2000, font=("Helvetica", 16))
    settings_2s.pack(pady=10)
    settings_3s = Radiobutton(root, text="3s", variable=delay, value=3000, font=("Helvetica", 16))
    settings_3s.pack(pady=10)
    settings_4s = Radiobutton(root, text="4s", variable=delay, value=4000, font=("Helvetica", 16))
    settings_4s.pack(pady=10)
    settings_8s = Radiobutton(root, text="8s", variable=delay, value=8000, font=("Helvetica", 16))
    settings_8s.pack(pady=10)
    settings_16s = Radiobutton(root, text="16s", variable=delay, value=16000, font=("Helvetica", 16))
    settings_16s.pack(pady=10)

    settings_apply_button =  Button(root, text = "Apply", command=lambda: settings_file_write(delay.get()), font=("Helvetica", 16))
    settings_mainmenu_button = Button(root, text = "Main Menu", command=lambda: settings_menu_destroy(0), font=("Helvetica", 16), cursor='hand2')
    settings_apply_button.pack(pady=10)
    settings_mainmenu_button.pack(pady=10)
    
    list_settings_menu_widgets = [title_pic, title_pic_delay, settings_apply_button, settings_mainmenu_button,
                                  settings_2s, settings_3s, settings_4s, settings_8s, settings_16s]


def settings_file_write(delay_value):
    global pic_change_delay_ms
    pic_change_delay_ms = delay_value
    try:
        # Here it should read config.txt and call the "config" parser
        with open('Config.txt','w') as config:
            config.write(delay_value)
    except:
        print("Error: Could not write in Config.txt")


def settings_file_read_apply():
    global pic_change_delay_ms
    try:
        with open('Config.txt','r') as config:
            config_content = config.read()
            # Here should call the config parser
            pic_change_delay_ms = int(config_content)
            print("settings_file_read_apply - pic_change_delay_ms", pic_change_delay_ms)
    except:
        print("WARNING: Config file not found, standard settings applied.")


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
    elif current_screen == 3: # 1 Image menu, 2 Image full screen, 3 My location, 4 Settings        
        call_location_script()
    elif current_screen == 4: # 1 Image menu, 2 Image full screen, 3 My location, 4 Settings        
        settings_menu()
    root.mainloop()# Main Loop


def load_files():
    load_mainmenu_images()
    settings_file_read_apply()
    

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



