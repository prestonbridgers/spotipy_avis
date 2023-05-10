import multiprocessing
from multiprocessing import Process, Value
import os
import pyaudio
import time
import wave
import librosa

song_place = Value('i', 0)


class MusicPlayer:
    def __init__(self):
        self.proc = None

    def play_song(self, audio_file):
        self.proc = Process(target=MusicPlayer.music_process_play_song, args=(audio_file,))
        self.proc.start()

    def terminate(self):
        self.stop_song()

    def stop_song(self):
        self.proc.terminate()

    @staticmethod
    def music_process_play_song(audio_file):
        audio_path = os.path.abspath(os.path.join('../audio', audio_file))
        print(f'Playing: {audio_path}')

        p = pyaudio.PyAudio()

        with wave.open(audio_path, 'rb') as wf:
            def callback(in_data, frame_count, time_info, status):
                global song_place
                data = wf.readframes(frame_count)
                place = wf.tell()
                song_place.value = place
                # print(f'place in song: {place}')      # Incremented by frame_count
                # print(f'frame_count: {frame_count}')  # 1024
                return data, pyaudio.paContinue

            audio_stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),  # 8
                                  channels=wf.getnchannels(),                         # 2
                                  rate=wf.getframerate(),                             # 44100Hz
                                  output=True,
                                  stream_callback=callback)

            while audio_stream.is_active():
                time.sleep(0.1)
