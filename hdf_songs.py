import os
import h5py
import pathlib


class HDFViewer:
    def __init__(self):
        pass

    @staticmethod
    def view_data(song_path: str):
        with h5py.File(song_path, "r") as f:
            metadata = list(f.keys())[1]

            print(f[metadata]['songs']['artist_name'][0].decode('utf-8'), end=',')
            print(f[metadata]['songs']['title'][0].decode('utf-8'))


def main():
    song_dir = pathlib.Path(os.path.abspath('./MillionSongSubset/data/'))
    songs = song_dir.rglob('*.h5')
    song_list = []
    for song in songs:
        song_list.append(os.path.join(song_dir, song))
    count = 0
    for song in song_list:
        print(f'{song}', end=',')
        HDFViewer.view_data(song)
        count += 1


if __name__ == "__main__":
    main()
