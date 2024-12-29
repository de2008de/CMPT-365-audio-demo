import sounddevice as sd
import numpy as np
from scipy.signal import resample
import threading


class VoiceRecorderApp:
    def __init__(self, root, gui_initializer, quantizer):
        self.root = root
        self.root.title("CMPT 365 - Voice Recorder")
        
        self.quantizer = quantizer
        
        self.recording = False
        self.audio_data = None
        self.original_audio_data = None
        self.resampled_data = None
        self.sampling_rate = 44100 
        self.resampled_rate = self.sampling_rate

        gui_initializer(self, root)

    def display_message(self, message, color="black"):
        self.message_label.config(text=message, fg=color)

    def set_buttons_state(self, state, exclude=None):
        if exclude is None:
            exclude = []
        for button in self.buttons:
            if button not in exclude:
                button.config(state=state)

    def threaded_action(self, func):
        def wrapper():
            self.set_buttons_state("disabled")
            thread = threading.Thread(target=self.run_action, args=(func,))
            thread.start()
        return wrapper

    def run_action(self, func):
        try:
            func()
        finally:
            if not self.recording:
                self.set_buttons_state("normal")
            else:
                self.set_buttons_state("disabled", exclude=[self.record_button])

    def toggle_recording(self):
        if not self.recording:
            self.set_buttons_state("disabled", exclude=[self.record_button])
            self.start_recording()
        else:
            self.set_buttons_state("normal")
            self.stop_recording()

    def start_recording(self):
        self.recording = True
        self.audio_data = None
        self.original_audio_data = None

        self.record_button.config(text="Stop", command=self.toggle_recording, bg="gray")

        def callback(indata, frames, time, status):
            if self.recording:
                if self.audio_data is None:
                    self.audio_data = indata.copy()
                else:
                    self.audio_data = np.concatenate((self.audio_data, indata))

        self.stream = sd.InputStream(callback=callback, channels=1, samplerate=self.sampling_rate)
        self.stream.start()
        self.display_message("Recording started!", "green")

    def stop_recording(self):
        if not self.recording:
            self.display_message("Not recording!", "red")
            return

        self.recording = False
        sd.stop()
        self.original_audio_data = self.audio_data.copy()  # Store the original data
        self.update_waveform(self.audio_data, self.ax1, self.sampling_rate)
        self.display_message("Recording stopped!", "green")

        self.record_button.config(text="Record", command=self.toggle_recording, bg="red")

    def resample_wave_file(self):
        if self.original_audio_data is None:
            self.display_message("No file loaded or recorded data available!", "red")
            return
        try:
            self.resampled_rate = int(self.sampling_rate_entry.get())
            quantization = int(self.quantization_entry.get())
            if self.resampled_rate <= 0 or not (1 <= quantization <= 16):
                raise ValueError
        except ValueError:
            self.display_message("Invalid sampling rate or quantization bits.", "red")
            return

        num_samples = int(len(self.original_audio_data) * self.resampled_rate / self.sampling_rate)
        self.resampled_data = resample(self.original_audio_data, num_samples, axis=0)

        self.resampled_data = self.quantizer.quantize(self.resampled_data, bits=quantization)

        self.update_waveform(self.resampled_data, self.ax2, self.resampled_rate)
        self.display_message("Resampling complete!", "green")

    def play_original(self):
        if self.audio_data is None:
            self.display_message("No original data to play!", "red")
            return

        sd.play(self.audio_data, samplerate=self.sampling_rate)
        sd.wait()
        self.display_message("Playing original audio.", "green")

    def play_resampled(self):
        if self.resampled_data is None:
            self.display_message("No resampled data to play!", "red")
            return
        
        upsampled_data = resample(self.resampled_data, int(len(self.resampled_data) * self.sampling_rate / self.resampled_rate))

        sd.play(upsampled_data, samplerate=int(self.sampling_rate))
        sd.wait()
        self.display_message("Playing resampled audio.", "green")

    def update_waveform(self, data, ax, rate):
        ax.clear()
        ax.plot(np.linspace(0, len(data) / rate, num=len(data)), data)
        ax.set_title(ax.get_title())
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Amplitude")
        self.canvas.draw()
