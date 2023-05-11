import glob
from tkinter import *
from tkinter import ttk
import json
import re

from music_player import MusicPlayer, song_place


class AVisGUI:
    def __init__(self):
        self.mp = MusicPlayer()
        self.music_playing = False
        self.data = None
        self.timbrebars = []
        self.pitchbars = []
        self.bar_height = 200
        self.pitchbars_startx = 10
        self.timbrebars_startx = 350
        self.window_width = 655
        self.window_height = 500
        self.beat_label_x = 10
        self.bar_label_x = 10
        self.section_label_x = 10
        self.beat_label_y = self.window_height - 190
        self.bar_label_y = self.beat_label_y + 20
        self.section_label_y = self.bar_label_y + 20

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Begin the GUI initialization ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.root = Tk()
        self.root.title("Spotify AVis")
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=5)
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.mainframe = ttk.Frame(self.root,
                                   width=self.window_width,
                                   height=self.window_height,
                                   borderwidth=5)
        self.mainframe.grid_rowconfigure(0, weight=1)
        self.mainframe.grid_columnconfigure(0, weight=1)
        self.mainframe.grid_columnconfigure(1, weight=1)
        self.mainframe.grid(column=0,
                            row=0)

        self.selected_audiofile = StringVar()
        self.audio_selector = ttk.Combobox(self.mainframe,
                                           textvariable=self.selected_audiofile,
                                           width=50)
        self.audio_selector['values'] = AVisGUI.get_audio_files()
        self.audio_selector.grid(column=1, row=0)

        self.audio_selector_label = ttk.Label(self.mainframe, text="Choose Audio:")
        self.audio_selector_label.grid(column=0, row=0)

        self.visual_canvas = Canvas(self.root, width=655, height=400, background='gray75')
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

        self.canvas_text = self.visual_canvas.create_text(5, 5, anchor='nw', text=f'Song Position: {song_place.value}')
        pitch_x_accum = self.pitchbars_startx
        timbre_x_accum = self.timbrebars_startx
        for i in range(12):
            self.pitchbars.append(self.visual_canvas.create_rectangle(pitch_x_accum, self.bar_height,
                                                                      pitch_x_accum + 20, self.bar_height,
                                                                      fill='black'))
            self.timbrebars.append(self.visual_canvas.create_rectangle(timbre_x_accum, self.bar_height,
                                                                       timbre_x_accum + 20, self.bar_height,
                                                                       fill='black'))
            pitch_x_accum += 25
            timbre_x_accum += 25

        self.canvas_pitchlbl = self.visual_canvas.create_text(170, 375, text=f'Segment Pitch Over Time')
        self.canvas_timbrelbl = self.visual_canvas.create_text(515, 375, text=f'Segment Timbre Over Time')

        self.canvas_beatlbl = self.visual_canvas.create_text(self.beat_label_x, self.beat_label_y, anchor='nw', text='Beat 0 Start: 0.0')
        self.canvas_barlbl = self.visual_canvas.create_text(self.bar_label_x, self.bar_label_y, anchor='nw', text='Bar 0 Start: 0.0')
        self.canvas_sectionlbl = self.visual_canvas.create_text(self.section_label_x, self.section_label_y, anchor='nw', text='Section 0 Start: 0.0')

        self.stop_button = ttk.Button(self.controls_frame, text="Stop", command=self.on_stop)
        self.stop_button.grid(column=2, row=0)
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ End the GUI initialization ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @staticmethod
    def get_audio_files():
        return glob.glob("../audio/*.wav")

    def on_play(self):
        self.music_playing = True
        file = self.selected_audiofile.get()
        song_name = re.match('^.*/(.*)\..*$', file)[1]
        print('song_name', song_name)
        analysis = f'../audio/{song_name}.json'

        # Load the data
        fd = open(analysis)
        self.data = json.load(fd)

        self.mp.play_song(file)

    def on_pause(self):
        self.music_playing = False
        self.mp.stop_song()

    def on_stop(self):
        self.music_playing = False
        self.mp.stop_song()

    def start(self):
        self.root.mainloop()
        self.mp.terminate()
