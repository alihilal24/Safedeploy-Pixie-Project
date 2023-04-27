import tkinter as tk
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM

class ImageSwitcher:
    def __init__(self, root):
        self.root = root
        self.current_image = 1
        self.images = ['flamegraph1.svg', 'flamegraph2.svg']
        self.create_widgets()

    def create_widgets(self):
        # create button to switch images
        self.switch_button = tk.Button(self.root, text="Switch Image", command=self.switch_image)
        self.switch_button.pack()

        # create label to display image
        self.image_label = tk.Label(self.root)
        self.image_label.pack()

        # display initial image
        self.display_image()

    def switch_image(self):
        # switch to next image
        self.current_image = (self.current_image + 1) % len(self.images)
        self.display_image()

    def display_image(self):
        # load image and display it in label
        drawing = svg2rlg(self.images[self.current_image])
        image = tk.PhotoImage(data=renderPM.drawToString(drawing, fmt="gif"))
        self.image_label.configure(image=image)
        self.image_label.image = image

# create root window
root = tk.Tk()

# create image switcher and run the main loop
app = ImageSwitcher(root)
root.mainloop()