import os
from tkinter import *
from tkinter import ttk

from music_player import MusicPlayer


class AVisGUI:
    def __init__(self):
        self.mp = MusicPlayer()
        self.root = Tk()
        self.root.title("Spotify AVis")
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=5)
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.mainframe = ttk.Frame(self.root,
                                   width=700,
                                   height=500,
                                   borderwidth=5)
        self.mainframe.grid_rowconfigure(0, weight=1)
        self.mainframe.grid_columnconfigure(0, weight=1)
        self.mainframe.grid_columnconfigure(1, weight=1)
        self.mainframe.grid(column=0,
                            row=0)

        self.selected_audiofile = StringVar()
        self.audio_selector = ttk.Combobox(self.mainframe,
                                           textvariable=self.selected_audiofile)
        self.audio_selector['values'] = AVisGUI.get_audio_files()
        self.audio_selector.grid(column=1, row=0)

        self.audio_selector_label = ttk.Label(self.mainframe, text="Choose Audio:")
        self.audio_selector_label.grid(column=0, row=0)

        self.visual_canvas = Canvas(self.root, width=700, height=400, background='gray75')
        self.visual_canvas.grid(column=0, row=1, sticky='n s e w')

        self.controls_frame = ttk.Frame(self.root, borderwidth=5)
        self.controls_frame.grid(column=0, row=2)
        self.controls_frame.grid_rowconfigure(0, weight=1)
        self.controls_frame.grid_columnconfigure(0, weight=1)
        self.controls_frame.grid_columnconfigure(1, weight=1)

        self.play_button = ttk.Button(self.controls_frame, text="Play", command=self.on_play)
        self.play_button.grid(column=0, row=0)

        self.pause_button = ttk.Button(self.controls_frame, text="Pause", command=self.on_pause)
        self.pause_button.grid(column=1, row=0)

        self.stop_button = ttk.Button(self.controls_frame, text="Stop", command=self.on_stop)
        self.stop_button.grid(column=2, row=0)

    @staticmethod
    def get_audio_files():
        return os.listdir("../audio")

    def on_play(self):
        file = self.selected_audiofile.get()
        self.mp.play_song(file)

    def on_pause(self):
        self.mp.stop_song()

    def on_stop(self):
        self.mp.stop_song()

    def start(self):
        self.root.mainloop()
        self.mp.terminate()


def main():
    app = AVisGUI()
    app.start()


if __name__ == "__main__":
    main()
