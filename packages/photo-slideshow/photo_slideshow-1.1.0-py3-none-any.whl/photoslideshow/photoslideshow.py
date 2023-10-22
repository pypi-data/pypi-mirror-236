import tkinter as tk
from photoslideshow.gui.app import App
global config


def main():
    root = tk.Tk()
    App(root)
    root.mainloop()

