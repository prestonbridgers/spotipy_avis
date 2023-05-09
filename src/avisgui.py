import os
import glob
from multiprocessing import Process
import time
from tkinter import *
from tkinter import ttk
import json

from music_player import MusicPlayer, song_place


class AVisGUI:
    def __init__(self):
        self.mp = MusicPlayer()
        self.music_playing = False
        self.data = None
        self.root = Tk()
        self.root.title("Spotify AVis")
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=5)
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.mainframe = ttk.Frame(self.root,
                                   width=655,
                                   height=500,
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
        self.bar_height = 200
        self.canvas_pitchbar1 = self.visual_canvas.create_rectangle(10,   self.bar_height, 30,  self.bar_height, fill='black')
        self.canvas_pitchbar2 = self.visual_canvas.create_rectangle(35,   self.bar_height, 55,  self.bar_height, fill='black')
        self.canvas_pitchbar3 = self.visual_canvas.create_rectangle(60,   self.bar_height, 80,  self.bar_height, fill='black')
        self.canvas_pitchbar4 = self.visual_canvas.create_rectangle(85,   self.bar_height, 105, self.bar_height, fill='black')
        self.canvas_pitchbar5 = self.visual_canvas.create_rectangle(110,  self.bar_height, 130, self.bar_height, fill='black')
        self.canvas_pitchbar6 = self.visual_canvas.create_rectangle(135,  self.bar_height, 155, self.bar_height, fill='black')
        self.canvas_pitchbar7 = self.visual_canvas.create_rectangle(160,  self.bar_height, 180, self.bar_height, fill='black')
        self.canvas_pitchbar8 = self.visual_canvas.create_rectangle(185,  self.bar_height, 205, self.bar_height, fill='black')
        self.canvas_pitchbar9 = self.visual_canvas.create_rectangle(210,  self.bar_height, 230, self.bar_height, fill='black')
        self.canvas_pitchbar10 = self.visual_canvas.create_rectangle(235, self.bar_height, 255, self.bar_height, fill='black')
        self.canvas_pitchbar11 = self.visual_canvas.create_rectangle(260, self.bar_height, 280, self.bar_height, fill='black')
        self.canvas_pitchbar12 = self.visual_canvas.create_rectangle(285, self.bar_height, 305, self.bar_height, fill='black')
        self.canvas_pitchlbl = self.visual_canvas.create_text(170, 375, text=f'Segment Pitch Over Time')

        self.canvas_timbrebar1 = self.visual_canvas.create_rectangle(350,   self.bar_height, 370,  self.bar_height, fill='black')
        self.canvas_timbrebar2 = self.visual_canvas.create_rectangle(375,   self.bar_height, 395,  self.bar_height, fill='black')
        self.canvas_timbrebar3 = self.visual_canvas.create_rectangle(400,   self.bar_height, 420,  self.bar_height, fill='black')
        self.canvas_timbrebar4 = self.visual_canvas.create_rectangle(425,   self.bar_height, 445, self.bar_height, fill='black')
        self.canvas_timbrebar5 = self.visual_canvas.create_rectangle(450,  self.bar_height, 470, self.bar_height, fill='black')
        self.canvas_timbrebar6 = self.visual_canvas.create_rectangle(475,  self.bar_height, 495, self.bar_height, fill='black')
        self.canvas_timbrebar7 = self.visual_canvas.create_rectangle(500,  self.bar_height, 520, self.bar_height, fill='black')
        self.canvas_timbrebar8 = self.visual_canvas.create_rectangle(525,  self.bar_height, 545, self.bar_height, fill='black')
        self.canvas_timbrebar9 = self.visual_canvas.create_rectangle(550,  self.bar_height, 570, self.bar_height, fill='black')
        self.canvas_timbrebar10 = self.visual_canvas.create_rectangle(575, self.bar_height, 595, self.bar_height, fill='black')
        self.canvas_timbrebar11 = self.visual_canvas.create_rectangle(600, self.bar_height, 620, self.bar_height, fill='black')
        self.canvas_timbrebar12 = self.visual_canvas.create_rectangle(625, self.bar_height, 645, self.bar_height, fill='black')
        self.canvas_timbrelbl = self.visual_canvas.create_text(515, 375, text=f'Segment Timbre Over Time')

        self.stop_button = ttk.Button(self.controls_frame, text="Stop", command=self.on_stop)
        self.stop_button.grid(column=2, row=0)

    @staticmethod
    def get_audio_files():
        return glob.glob("../audio/*.wav")

    def on_play(self):
        self.music_playing = True
        file = self.selected_audiofile.get()

        # Load the data
        fd = open('../audio/meeting_the_master.json')
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


def maprange(value, inMin, inMax, outMin, outMax):
    return outMin + (((value - inMin) / (inMax - inMin)) * (outMax - outMin))


def gui_updater(app):
    app.visual_canvas.itemconfigure(app.canvas_text, text=f'Song Position: {song_place.value}')
    if app.data is not None:
        min_segment = 0
        max_segment = len(app.data['segments'])
        min_frame = 0
        max_frame = 6885179
        current_segment = int(maprange(song_place.value, min_frame, max_frame, min_segment, max_segment))
        
        timbre_1 = app.data['segments'][current_segment]['timbre'][0]
        timbre_2 = app.data['segments'][current_segment]['timbre'][1]
        timbre_3 = app.data['segments'][current_segment]['timbre'][2]
        timbre_4 = app.data['segments'][current_segment]['timbre'][3]
        timbre_5 = app.data['segments'][current_segment]['timbre'][4]
        timbre_6 = app.data['segments'][current_segment]['timbre'][5]
        timbre_7 = app.data['segments'][current_segment]['timbre'][6]
        timbre_8 = app.data['segments'][current_segment]['timbre'][7]
        timbre_9 = app.data['segments'][current_segment]['timbre'][8]
        timbre_10 = app.data['segments'][current_segment]['timbre'][9]
        timbre_11 = app.data['segments'][current_segment]['timbre'][10]
        timbre_12 = app.data['segments'][current_segment]['timbre'][11]

        pitch_1  = app.data['segments'][current_segment]['pitches'][0]
        pitch_2  = app.data['segments'][current_segment]['pitches'][1]
        pitch_3  = app.data['segments'][current_segment]['pitches'][2]
        pitch_4  = app.data['segments'][current_segment]['pitches'][3]
        pitch_5  = app.data['segments'][current_segment]['pitches'][4]
        pitch_6  = app.data['segments'][current_segment]['pitches'][5]
        pitch_7  = app.data['segments'][current_segment]['pitches'][6]
        pitch_8  = app.data['segments'][current_segment]['pitches'][7]
        pitch_9  = app.data['segments'][current_segment]['pitches'][8]
        pitch_10 = app.data['segments'][current_segment]['pitches'][9]
        pitch_11 = app.data['segments'][current_segment]['pitches'][10]
        pitch_12 = app.data['segments'][current_segment]['pitches'][11]

        app.visual_canvas.delete(app.canvas_pitchbar1)
        app.visual_canvas.delete(app.canvas_pitchbar2)
        app.visual_canvas.delete(app.canvas_pitchbar3)
        app.visual_canvas.delete(app.canvas_pitchbar4)
        app.visual_canvas.delete(app.canvas_pitchbar5)
        app.visual_canvas.delete(app.canvas_pitchbar6)
        app.visual_canvas.delete(app.canvas_pitchbar7)
        app.visual_canvas.delete(app.canvas_pitchbar8)
        app.visual_canvas.delete(app.canvas_pitchbar9)
        app.visual_canvas.delete(app.canvas_pitchbar10)
        app.visual_canvas.delete(app.canvas_pitchbar11)
        app.visual_canvas.delete(app.canvas_pitchbar12)

        app.visual_canvas.delete(app.canvas_timbrebar1)
        app.visual_canvas.delete(app.canvas_timbrebar2)
        app.visual_canvas.delete(app.canvas_timbrebar3)
        app.visual_canvas.delete(app.canvas_timbrebar4)
        app.visual_canvas.delete(app.canvas_timbrebar5)
        app.visual_canvas.delete(app.canvas_timbrebar6)
        app.visual_canvas.delete(app.canvas_timbrebar7)
        app.visual_canvas.delete(app.canvas_timbrebar8)
        app.visual_canvas.delete(app.canvas_timbrebar9)
        app.visual_canvas.delete(app.canvas_timbrebar10)
        app.visual_canvas.delete(app.canvas_timbrebar11)
        app.visual_canvas.delete(app.canvas_timbrebar12)

        app.canvas_pitchbar1 = app.visual_canvas.create_rectangle(10,   app.bar_height - 150 * pitch_1, 30,   app.bar_height, fill='black')
        app.canvas_pitchbar2 = app.visual_canvas.create_rectangle(35,   app.bar_height - 150 * pitch_2, 55,   app.bar_height, fill='black')
        app.canvas_pitchbar3 = app.visual_canvas.create_rectangle(60,   app.bar_height - 150 * pitch_3, 80,   app.bar_height, fill='black')
        app.canvas_pitchbar4 = app.visual_canvas.create_rectangle(85,   app.bar_height - 150 * pitch_4, 105,  app.bar_height, fill='black')
        app.canvas_pitchbar5 = app.visual_canvas.create_rectangle(110,  app.bar_height - 150 * pitch_5, 130,  app.bar_height, fill='black')
        app.canvas_pitchbar6 = app.visual_canvas.create_rectangle(135,  app.bar_height - 150 * pitch_6, 155,  app.bar_height, fill='black')
        app.canvas_pitchbar7 = app.visual_canvas.create_rectangle(160,  app.bar_height - 150 * pitch_7, 180,  app.bar_height, fill='black')
        app.canvas_pitchbar8 = app.visual_canvas.create_rectangle(185,  app.bar_height - 150 * pitch_8, 205,  app.bar_height, fill='black')
        app.canvas_pitchbar9 = app.visual_canvas.create_rectangle(210,  app.bar_height - 150 * pitch_9, 230,  app.bar_height, fill='black')
        app.canvas_pitchbar10 = app.visual_canvas.create_rectangle(235, app.bar_height - 150 * pitch_10, 255, app.bar_height, fill='black')
        app.canvas_pitchbar11 = app.visual_canvas.create_rectangle(260, app.bar_height - 150 * pitch_11, 280, app.bar_height, fill='black')
        app.canvas_pitchbar12 = app.visual_canvas.create_rectangle(285, app.bar_height - 150 * pitch_12, 305, app.bar_height, fill='black')

        app.canvas_timbrebar1 = app.visual_canvas.create_rectangle(350,   app.bar_height - timbre_1, 370,  app.bar_height, fill='black')
        app.canvas_timbrebar2 = app.visual_canvas.create_rectangle(375,   app.bar_height - timbre_2, 395,  app.bar_height, fill='black')
        app.canvas_timbrebar3 = app.visual_canvas.create_rectangle(400,   app.bar_height - timbre_3, 420,  app.bar_height, fill='black')
        app.canvas_timbrebar4 = app.visual_canvas.create_rectangle(425,   app.bar_height - timbre_4, 445,  app.bar_height, fill='black')
        app.canvas_timbrebar5 = app.visual_canvas.create_rectangle(450,   app.bar_height - timbre_5, 470,  app.bar_height, fill='black')
        app.canvas_timbrebar6 = app.visual_canvas.create_rectangle(475,   app.bar_height - timbre_6, 495,  app.bar_height, fill='black')
        app.canvas_timbrebar7 = app.visual_canvas.create_rectangle(500,   app.bar_height - timbre_7, 520,  app.bar_height, fill='black')
        app.canvas_timbrebar8 = app.visual_canvas.create_rectangle(525,   app.bar_height - timbre_8, 545,  app.bar_height, fill='black')
        app.canvas_timbrebar9 = app.visual_canvas.create_rectangle(550,   app.bar_height - timbre_9, 570,  app.bar_height, fill='black')
        app.canvas_timbrebar10 = app.visual_canvas.create_rectangle(575,  app.bar_height - timbre_10, 595,  app.bar_height, fill='black')
        app.canvas_timbrebar11 = app.visual_canvas.create_rectangle(600,  app.bar_height - timbre_11, 620,  app.bar_height, fill='black')
        app.canvas_timbrebar12 = app.visual_canvas.create_rectangle(625,  app.bar_height - timbre_12, 645,  app.bar_height, fill='black')

    app.root.after(50, gui_updater, app)


def main():
    #multiprocessing.set_start_method('spawn')
    app = AVisGUI()
    app.root.after(50, gui_updater, app)
    app.start()


if __name__ == "__main__":
    main()
