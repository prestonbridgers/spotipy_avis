import librosa
import soundfile as sf
import os

target_sr = 22050
song_name = 'heat_above'
new_name = f'{song_name}_22050.wav'
song_path = os.path.join('../audio/', f'{song_name}.wav')
new_path = os.path.join('../audio/', new_name)

y, _ = librosa.load(song_path, sr=target_sr)

sf.write(file=new_path,
         data=y,
         samplerate=target_sr)
