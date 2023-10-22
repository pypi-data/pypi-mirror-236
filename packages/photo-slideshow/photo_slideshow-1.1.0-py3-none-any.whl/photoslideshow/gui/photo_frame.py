import tkinter as tk
from PIL import Image, ImageTk, ImageOps
import photoslideshow.common.photo as fp
from photoslideshow import config
from importlib.resources import files as files_rs
import io


class PhotoFrame(tk.Frame):
    """
    Creates tkinter's frame with the photo with all necessary functions
    """
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.generate_showzone()
        self.lbl_img.bind('<Configure>', self.handle_resize_image)

    def generate_showzone(self):
        """
        section to show the pictures
        """
        self.frm_showzone = tk.Frame(master=self.parent, bg=config['photo'].get('background.color', 'black'))
        self.frm_showzone.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
        eml_photo = files_rs('resources').joinpath('photoslideshow.png').read_bytes()
        self.image = Image.open(io.BytesIO(eml_photo))
        self.copy_of_image = self.image.copy()
        self.photo = ImageTk.PhotoImage(self.image)
        self.lbl_img = tk.Label(self.frm_showzone, image=self.photo)
        self.lbl_img.pack(fill=tk.BOTH, expand=tk.YES)

    def handle_resize_image(self, event):
        """
        Resize the image keeping its original proportions
        """
        # rotate image based on the exif information
        self.copy_of_image = ImageOps.exif_transpose(self.copy_of_image)
        # new_width, new_height = fp.calc_resize(self.copy_of_image.width, self.copy_of_image.height, event.width, event.height)  # event dimensions doesn't work with tkinter with "after" method
        new_width, new_height = fp.calc_resize(self.copy_of_image.width, self.copy_of_image.height, self.lbl_img.winfo_width(), self.lbl_img.winfo_height())
        self.image = self.copy_of_image.resize((int(new_width), int(new_height)), Image.LANCZOS)
        self.photo = ImageTk.PhotoImage(self.image)
        self.lbl_img.config(image=self.photo, bg=config['photo'].get('background.color', 'black'))
        self.lbl_img.image = self.photo  # avoid garbage collection

    def change_photo(self, new_photo):
        self.copy_of_image = Image.open(new_photo)
        self.lbl_img.event_generate('<Configure>')
        # root.event_generate("<<Foo>>", when="tail")