import tkinter as tk
import webbrowser


class About(tk.Toplevel):
    """
    Window to show photos in fullscreen mode
    """
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.grab_set()

        def callurl(url):
            webbrowser.open_new_tab(url)

        tk.Label(master=self, text="Version: 1.1.0").pack(padx=20, pady=(20,5))
        tk.Label(master=self, text="Author: Mateusz Poślednik").pack(padx=20, pady=5, anchor="w")

        url_project = "https://pypi.org/project/photo-slideshow/"
        self.frm_project_url = tk.Frame(master=self)
        self.frm_project_url.pack(padx=20, pady=5, anchor="w")
        tk.Label(master=self.frm_project_url, text="Project url: ").pack(side=tk.LEFT)
        self.link_project = tk.Label(master=self.frm_project_url, text=url_project, font=('Helvetica'), fg="blue", cursor="hand2")
        self.link_project.pack(padx=(0,20), pady=5, anchor="w")

        tk.Label(master=self, text="License: MIT").pack(padx=20, pady=5, anchor="w")

        url_author = "https://matpos.pythonanywhere.com/"
        self.frm_author_url = tk.Frame(master=self)
        self.frm_author_url.pack(padx=20, pady=5, anchor="w")
        tk.Label(master=self.frm_author_url, text="Author contact: ").pack(side=tk.LEFT)
        self.link_author = tk.Label(master=self.frm_author_url, text=url_project, font=('Helvetica'), fg="blue", cursor="hand2")
        self.link_author.pack(padx=(0, 20), pady=5, anchor="w")

        tk.Label(master=self, text="Copyright by: Mateusz Poślednik@2023").pack(padx=20, pady=5)

        tk.Button(master=self, text="Close", command=lambda: self.destroy()).pack(padx=20, pady=20)

        self.link_project.bind("<Button-1>", lambda e: callurl(url_project))
        self.link_author.bind("<Button-1>", lambda e: callurl(url_author))

