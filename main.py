import tkinter as tk
from models.app import VoiceRecorderApp
from models.quantizer import UniformQuantizer
from models.gui import gui_initializer


def main():
    root = tk.Tk()
    VoiceRecorderApp(root, gui_initializer, UniformQuantizer())
    root.mainloop()


if __name__ == "__main__":
    main()
