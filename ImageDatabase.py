## 
## 

from tkinter import *
from PIL import ImageTk, Image
from tkinter import filedialog

root = Tk()
root.title("## Test ##")
#root.attributes('-fullscreen', True)

def open():
    global my_image
    root.filename = filedialog.askopenfilename(initialdir="/home/pi/Pictures", title="Select a file", filetypes=(("all files", "*.*"),("png files", "*.png"),("jpg files", "*.jpg")) )
    my_lable = Label(root, text=root.filename).pack()
    #my_image = ImageTk.PhotoImage(Image.open(root.filename))
    my_image = ImageTk.PhotoImage(Image.open(root.filename), size='50x50')
    #my_image = ImageTk.PhotoImage(Image.open(root.filename))
    
    #my_image = my_image1.subsample(50)
    #my_image = subsample(my_image1)
    my_image_lable = Label(image=my_image).pack()
    print(root.winfo_geometry())
    print("Window With ", root.winfo_screenwidth())
    print("Window Heigh ", root.winfo_screenheight())
    print("Window With ", root.winfo_width())
    print("Window Heigh ", root.winfo_height())
    print(f"Image width {my_image.width()} pixels")
    print(f"Image height {my_image.height()} pixels")


button_open = Button(root, text = "Open", command=open).pack()

button_quit = Button(root, text = "Exit Program", command=root.destroy).pack()

# Main Loop
root.mainloop()