## 
## 

############################### Imports ##############################################################################
from tkinter import *
from PIL import ImageTk, Image
from tkinter import filedialog

############################### Definitions - Main Window ####################################################################
root = Tk()

############################### Settings ##############################################################################
#root.minsize(900, 900)
root.geometry("1000x1000")
root.title("## Test ##")
#root.attributes('-fullscreen', True)
image_location = "Images/background_example.jpeg"
image_backbutton_location = 'Images/right_transparent_arrow.png'
image_forwardbutton_location = 'Images/right_transparent_arrow.png'
button_subsample_factor = 8

############################### Definitions - Frames ####################################################################
frame_image = LabelFrame(root, border=0) # These padx and pady goes inside the frame
#frame_image.attributes('-fullscreen', True)
frame_image.pack(fill = 'x')
#frame_image.grid(row=0, column=0, sticky="ew")
frame_menu = LabelFrame(root, border=0) # These padx and pady goes inside the frame
#frame_menu.attributes('-fullscreen', True)
frame_menu.pack(fill = 'x')
#frame_menu.grid(row=1, column=0, sticky="ew")

Grid.columnconfigure(frame_menu, index=0, weight=1) # index is the row number
Grid.columnconfigure(frame_menu, index=1, weight=1) # index is the row number

############################### Definitions - Lables ####################################################################
#my_label = Label(root,text='')
#my_label.pack()

############################### Definitions - Functions #################################################################
def fullscreen():
    return

############################### Frame Image ##############################################################################
print("Window With ", root.winfo_screenwidth())
print("Window Heigh ", root.winfo_screenheight())
win_width = root.winfo_screenwidth()
win_height = root.winfo_screenheight()

image_resized = ImageTk.PhotoImage(Image.open(image_location).resize((400, 400), Image.ANTIALIAS)) # Open and resize image
image_resized_lable = Label(frame_image, image=image_resized).pack() # Place resized image onto screen


############################### Frame Menu ##############################################################################
image_forwardbutton = PhotoImage(file=image_forwardbutton_location).subsample(button_subsample_factor, button_subsample_factor)
image_backbutton = PhotoImage(file=image_backbutton_location).subsample(button_subsample_factor, button_subsample_factor)

#backbutton = Button(frame_menu, image=image_backbutton, command=thing2, borderwidth=0, cursor='hand2')
backbutton = Button(frame_menu, text = "Back", command=root.destroy, cursor='hand2')
fullscreenbutton = Button(frame_menu, text = "Full Screen", command=fullscreen, cursor='hand2')
exitbutton = Button(frame_menu, text = "Exit Program", command=root.destroy, cursor='hand2')
menubutton = Button(frame_menu, text = "Menu", command=root.destroy, cursor='hand2')
#forwardbutton = Button(frame_menu, image=image_forwardbutton, command=thing1, borderwidth=0, cursor='hand2')
forwardbutton = Button(frame_menu, text = "Forward", command=root.destroy, cursor='hand2')

side_buttons = [backbutton, forwardbutton]
middle_buttons = [fullscreenbutton, exitbutton, menubutton]

Grid.rowconfigure(frame_menu, index=0, weight=2) # index is the row number
Grid.columnconfigure(frame_menu, index=0, weight=2)
Grid.columnconfigure(frame_menu, index=4, weight=2)
backbutton.grid(row=0, column=0, sticky="ew", padx=1, pady=1)
forwardbutton.grid(row=0, column=4, sticky="ew", padx=1, pady=1)
    
Grid.rowconfigure(frame_menu, index=0, weight=1) # index is the row number   
for index_b, button in enumerate(middle_buttons):
    Grid.columnconfigure(frame_menu, index=index_b+1, weight=1)
    button.grid(row=0, column=index_b+1, sticky="ew", padx=1, pady=1)
   

# Main Loop
root.mainloop()