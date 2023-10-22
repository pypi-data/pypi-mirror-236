import os
import random
import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
import photoslideshow.common.files_handler as files
from photoslideshow import config
from photoslideshow.gui.photo_frame import PhotoFrame
from photoslideshow.gui.window_about import About
from photoslideshow.gui.window_config import AppConfig
from photoslideshow.gui.window_fullscreen import PhotoFullscreen
from importlib.resources import files as files_rs


class App:
    def __init__(self, parent, *args, **kwargs):
        self.root = parent
        self.configure()

        self.generate_path()
        self.frm_photo = PhotoFrame(self.root)

        self.root.bind("<F11>", self.handle_button_start)
        self.root.bind("<Escape>", self.handle_keypress_esc)

    def configure(self):
        self.root.title("photo-sliedshow")
        # self.root.wm_iconphoto(True, tk.PhotoImage(master=self.root, file=config['gui'].get('icon')))
        eml_ico = files_rs('resources').joinpath('photoslideshow_ico.png').read_bytes()
        self.root.wm_iconphoto(True, tk.PhotoImage(master=self.root, data=eml_ico))
        self.root.geometry(config['gui'].get('window.width', '800') + "x" + config['gui'].get('window.height', '600'))
        self.is_running = False

    def generate_path(self):
        """
        section for files, path info input
        """
        self.frm_path = tk.Frame(master=self.root, height=31)
        self.frm_path.pack()
        tk.Label(master=self.frm_path, text="Folder: ").pack(side=tk.LEFT, padx=4)
        self.folder_path = tk.StringVar(value=config['path'].get('lastfolder', str(Path.home())))
        self.ent_path = tk.Entry(master=self.frm_path, width=30, textvariable=self.folder_path)
        self.ent_path.pack(side=tk.LEFT, padx=4)
        self.btn_browse = tk.Button(master=self.frm_path, text="Browse...", command=self.handle_button_browse)
        self.btn_browse.pack(side=tk.LEFT, padx=4)
        self.is_fullscreen = tk.IntVar(value=1)
        self.chk_fullscreen = tk.Checkbutton(self.frm_path, text='Fullscreen mode', variable=self.is_fullscreen, onvalue=1, offvalue=0)
        self.chk_fullscreen.pack(side=tk.LEFT, padx=4)
        self.btn_start = tk.Button(master=self.frm_path, text="▶", command=self.handle_button_start)
        self.btn_start.pack(side=tk.LEFT, padx=4)
        self.btn_stop = tk.Button(master=self.frm_path, text="◼", command=self.handle_button_stop)
        self.btn_stop.pack(side=tk.LEFT, padx=4)
        self.btn_config = tk.Button(master=self.frm_path, text="⛭", command=self.handle_button_config)
        self.btn_config.pack(side=tk.LEFT, padx=4)
        self.btn_about = tk.Button(master=self.frm_path, text="About", command=self.handle_button_about)
        self.btn_about.pack(side=tk.LEFT, padx=4)

    def handle_keypress_esc(self, event):
        self.handle_button_stop()

    def handle_button_browse(self):
        folder_name = filedialog.askdirectory(initialdir=self.folder_path.get())
        # if dialog box has been closed or cancelled without confirmation
        if isinstance(folder_name, str) and len(folder_name) > 0:
            self.folder_path.set(folder_name)

    def handle_button_stop(self):
        try:
            # if we are not in the fullscreen mode, the object doesn't exist
            self.win_slides.destroy()
        except:
            pass
        self.is_running = False

    def handle_button_start(self, event=None):
        try:
            if not os.path.isdir(self.folder_path.get()):
                tk.messagebox.showerror(title="Error", message="Given folder does not exist")
                return
            patterns = tuple(config['path'].get('filespattern', '*.jpg,*.jpeg').split(','))
            self.photos = files.scan_folder(self.folder_path.get(), patterns)
            if len(self.photos) == 0:
                tk.messagebox.showerror(title="Error", message="Given folder does not contains any images. Check also the file extensions in the settings.")
                return

            # the files are collected, it means that the folder exists, so we can safely store it in the config file
            config['path']['lastfolder'] = self.folder_path.get()

            # save new path to the config
            files.save_config(config)

            if self.is_fullscreen.get() == 1:
                self.win_slides = PhotoFullscreen(self.root, self.photos)
                self.run_slideshow(self.win_slides, 0)  # start from the first photo
            else:
                self.is_running = True
                self.run_slideshow(self, 0)  # start from the first photo
        except Exception as e:
            tk.messagebox.showerror(title="Error", message=str(e))

    def run_slideshow(self, container, i):
        if container.is_running:
            container.frm_photo.change_photo(container.photos[i])
            if config['photo'].getboolean('slideshow.random'):
                i = random.randint(0, len(container.photos) - 1)
            elif i + 1 < len(container.photos):
                i += 1
            else:
                i = 0
            container.frm_photo.after(config['photo'].getint('slideshow.time.milisec', 3000), self.run_slideshow, container, i)

    def handle_button_config(self):
        AppConfig(self.root)

    def handle_button_about(self):
        About(self.root)
