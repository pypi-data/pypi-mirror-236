import tkinter as tk
from photoslideshow.gui.photo_frame import PhotoFrame
import re


class PhotoFullscreen(tk.Toplevel):
    """
    Window to show photos in fullscreen mode
    """
    def __init__(self, parent, photos):
        super().__init__(parent)
        self.parent = parent
        self.photos = photos
        self.title("photo-sliedshow-fullscreen")
        self.attributes('-fullscreen', True)  # testowo wylaczone
        self.is_running = True

        self.frm_photo = PhotoFrame(self)
        self.bind("<Escape>", self.handle_keypress_esc)

        # get window geometry of the main window, string as [width]x[height]+[left]+[top]
        geometry = self.parent.winfo_geometry()
        geometry_matched = re.findall(r'\d+', geometry)
        parent_h = geometry_matched[0]
        parent_w = geometry_matched[1]
        parent_p = geometry_matched[2]  # window position from the left

        # set fullscrean on the same monitor where the main window is shown
        self.geometry('%sx%s+%s+%s'%(parent_h, parent_w, parent_p, 0))

    def handle_keypress_esc(self, event):
        """Print the character associated to the key pressed"""
        self.destroy()
