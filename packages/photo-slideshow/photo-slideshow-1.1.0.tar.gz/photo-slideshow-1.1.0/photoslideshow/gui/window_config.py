import tkinter as tk
from tkinter import colorchooser, messagebox

from photoslideshow.common.files_handler import save_config
from photoslideshow import config
from PIL import Image


class AppConfig(tk.Toplevel):
    """
    Window for settings
    """
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.grab_set()

        self.config()
        self.generate_settings()
        self.generate_supported_files()
        self.generate_exit_buttons()

        self.bind("<Escape>", self.handle_keypress_esc)

    def config(self):
        self.title("photo-sliedshow-settings")
        self.geometry('600x550')

    def generate_exit_buttons(self):
        self.frm_buttons = tk.Frame(master=self)
        self.frm_buttons.pack(pady=15)
        self.btn_ok = tk.Button(master=self.frm_buttons, text="OK", command=self.handle_button_ok)
        self.btn_ok.pack(side=tk.LEFT, padx=4)
        self.btn_cancel = tk.Button(master=self.frm_buttons, text="Cancel", command=self.handle_keypress_esc)
        self.btn_cancel.pack(side=tk.LEFT, padx=4)

    def generate_settings(self):
        self.frm_label_main = tk.LabelFrame(master=self, text="Settings", padx=20, pady=20)
        self.frm_label_main.pack(padx=10, pady=5, fill=tk.X)

        self.frm_settings1 = tk.Frame(master=self.frm_label_main)
        self.frm_settings1.pack(ipadx=20, ipady=5, fill=tk.X)
        tk.Label(master=self.frm_settings1, text="Background color: ").pack(side=tk.LEFT, padx=4)
        self.color_bg = config['photo'].get('background.color', 'black')
        self.btn_color_bg = tk.Button(master=self.frm_settings1, text="◼", bg=self.color_bg, fg=self.color_bg, command=self.handle_button_color_bg)
        self.btn_color_bg.pack(side=tk.LEFT, padx=4)

        self.frm_settings2 = tk.Frame(master=self.frm_label_main)
        self.frm_settings2.pack(ipadx=20, ipady=5, fill=tk.X)
        tk.Label(master=self.frm_settings2, text="Time to show each photo in miliseconds: ").pack(side=tk.LEFT, padx=4)
        self.slideshow_time = tk.StringVar(value=config['photo'].getint('slideshow.time.milisec', 3000))
        self.ent_slideshow_time = tk.Entry(master=self.frm_settings2, width=10, textvariable=self.slideshow_time)
        self.ent_slideshow_time.pack(side=tk.LEFT, padx=4)

        self.frm_settings3 = tk.Frame(master=self.frm_label_main)
        self.frm_settings3.pack(ipadx=20, ipady=5, fill=tk.X)
        self.is_random = tk.BooleanVar(value=config['photo'].getboolean('slideshow.random'))
        tk.Label(master=self.frm_settings3, text="Show photos in random order:").pack(side=tk.LEFT, padx=4)
        self.chk_random = tk.Checkbutton(self.frm_settings3, variable=self.is_random, onvalue=1, offvalue=0)
        self.chk_random.pack(side=tk.LEFT, padx=0)

    def generate_supported_files(self):
        self.frm_label_patterns = tk.LabelFrame(master=self, text="Files to read", padx=20, pady=20)
        self.frm_label_patterns.pack(padx=10, pady=5, fill=tk.BOTH)

        all_formats = Image.registered_extensions()
        self.supported_formats = [ex for ex, f in all_formats.items() if f in Image.OPEN]
        self.supported_formats.sort()
        self.chk_pattern_list = []
        config_patterns = tuple(config['path'].get('filespattern', '*.jpg,*.jpeg').replace('*','').split(','))
        i = 0
        frm_current = None
        for format in self.supported_formats:
            self.chk_pattern_list.append(tk.BooleanVar(value=format in config_patterns))
            if i % 10 == 0:  # every 10 checkboxes generate new line
                frm_current = tk.Frame(master=self.frm_label_patterns)
                frm_current.pack(ipadx=20, ipady=5, fill=tk.X)
            tk.Checkbutton(frm_current, variable=self.chk_pattern_list[i], text=format, onvalue=1, offvalue=0).pack(side=tk.LEFT, padx=0)
            i += 1

    def handle_button_color_bg(self):
        color_buffer = colorchooser.askcolor(parent=self, color=self.color_bg)[1]
        if color_buffer is not None:
            self.color_bg = color_buffer
        self.btn_color_bg.configure(bg=self.color_bg, fg=self.color_bg)

    def handle_keypress_esc(self, event=None):
        """Print the character associated to the key pressed"""
        self.destroy()

    def handle_button_ok(self):
        """
        Save new settings
        """
        try:
            config['photo']['background.color'] = self.color_bg
            config['photo']['slideshow.time.milisec'] = self.slideshow_time.get() if self.slideshow_time.get().isdigit() else "3000"
            config['photo']['slideshow.random'] = str(self.is_random.get())

            patterns = ''
            for i in range(len(self.chk_pattern_list)):
                if self.chk_pattern_list[i].get():  # is checked
                    patterns = patterns + '*' + self.supported_formats[i] + ","
            config['path']['filespattern'] = patterns[:-1]

            save_config(config)
            self.destroy()
        except Exception as error:
            tk.messagebox.showerror(title="Error", message=str(error))
