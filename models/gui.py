import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os


def gui_initializer(self, root):
    self.button_font_size = 14

    self.logo_image = tk.PhotoImage(file="resources/utj_logo.png")
    self.logo_image = self.logo_image.subsample(4, 4)
    
    self.logo_label = tk.Label(root, image=self.logo_image)
    self.logo_label.pack(pady=10)
    self.root.iconphoto(False, self.logo_image)
    self.logo_text = tk.Label(root, text="Developed by Undergrad Tutorial Journal", font=("TkDefaultFont", 16))
    self.logo_text.pack(pady=5)
    
    self.record_button = tk.Button(root, text="Record", command=self.toggle_recording, bg="red", fg="white", font=("TkDefaultFont", self.button_font_size))
    self.record_button.pack(pady=10)

    self.sampling_rate_label = tk.Label(root, text="Enter new sampling rate (Hz):", font=("TkDefaultFont", self.button_font_size))
    self.sampling_rate_label.pack(pady=5)

    self.sampling_rate_entry = tk.Entry(root, font=("TkDefaultFont", self.button_font_size))
    self.sampling_rate_entry.insert(0, "44100")
    self.sampling_rate_entry.pack(pady=5)

    self.original_file_size_label = tk.Label(root, text="Original File size (KB):", font=("TkDefaultFont", self.button_font_size)) 
    self.compressed_size_label = tk.Label(root, text="Compressed size (KB):", font=("TkDefaultFont", self.button_font_size))
    self.original_file_size_label.pack(pady=5)
    self.compressed_size_label.pack(pady=5)

    self.quantization_label = tk.Label(root, text="Enter quantization bits (1 to 16):", font=("TkDefaultFont", self.button_font_size))
    self.quantization_label.pack(pady=5)

    self.quantization_entry = tk.Entry(root, font=("TkDefaultFont", self.button_font_size))
    self.quantization_entry.insert(0, "16")
    self.quantization_entry.pack(pady=5)

    self.resample_button = tk.Button(root, text="Resample", command=self.threaded_action(self.resample_wave_file), bg="green", fg="white", font=("TkDefaultFont", self.button_font_size))
    self.resample_button.pack(pady=10)

    self.play_original_button = tk.Button(root, text="Play Original", command=self.threaded_action(self.play_original), bg="red", fg="white", font=("TkDefaultFont", self.button_font_size))
    self.play_original_button.pack(pady=5)

    self.play_resampled_button = tk.Button(root, text="Play Resampled", command=self.threaded_action(self.play_resampled), bg="green", fg="white", font=("TkDefaultFont", self.button_font_size))
    self.play_resampled_button.pack(pady=5)

    # Add matplotlib figures for waveform visualization
    self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(5, 4))
    self.fig.tight_layout(pad=3.0)
    self.ax1.set_title("Original Waveform")
    self.ax2.set_title("Resampled Waveform")

    self.canvas = FigureCanvasTkAgg(self.fig, master=root)
    self.canvas.get_tk_widget().pack()

    # Add a message label
    self.message_label = tk.Label(root, text="", fg="black")
    self.message_label.pack(pady=10)

    self.buttons = [
        self.record_button,
        self.resample_button,
        self.play_original_button,
        self.play_resampled_button,
    ]
    
    # Create a menu bar
    self.menu_bar = tk.Menu(root)
    root.config(menu=self.menu_bar)

    # Create a Help menu
    def show_about():
        about_message = "CMPT 365 - Voice Recorder\nDeveloped by Undergrad Tutorial Journal\nVersion: 1.0.0\n1. Record audio by clicking the Record button.\n2. Resample the recorded audio by entering a new sampling rate and quantization bits.\n3. Play the original and resampled audio using the Play Original and Play Resampled buttons."
        tk.messagebox.showinfo("About", about_message)
    self.help_menu = tk.Menu(self.menu_bar, tearoff=0)
    self.menu_bar.add_cascade(label="Help", menu=self.help_menu)
    self.help_menu.add_command(label="About", command=show_about)

    def on_close():
        self.running = False
        self.recording = False
        if hasattr(self, 'stream') and self.stream.active:
            self.stream.stop()
            self.stream.close()
        self.root.destroy()  # Destroy the main Tkinter window
        os._exit(0) 
    
    root.protocol("WM_DELETE_WINDOW", on_close)
