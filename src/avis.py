from gui import AVisGUI
from music_player import song_place


def gui_updater(app):
    current_time = song_place.value / 22050
    app.visual_canvas.itemconfigure(app.canvas_text, text=f'Song Position: {current_time}')
    if app.data is not None:

        # Find the proper segment to show (slow)
        current_segment = None
        prev_seg = app.data['segments'][0]
        for seg in app.data['segments']:
            if prev_seg['start'] <= current_time < seg['start']:
                current_segment = prev_seg
                break
            else:
                prev_seg = seg

        timbres = []
        pitches = []
        pitch_x_accum = app.pitchbars_startx
        timbre_x_accum = app.timbrebars_startx
        for i in range(12):
            timbres.append(current_segment['timbre'][i])
            pitches.append(current_segment['pitches'][i])
            app.visual_canvas.delete(app.timbrebars[i])
            app.visual_canvas.delete(app.pitchbars[i])

            app.pitchbars[i] = app.visual_canvas.create_rectangle(pitch_x_accum, app.bar_height - 150 * pitches[i],
                                                                  pitch_x_accum + 20, app.bar_height, fill='black')
            app.timbrebars[i] = app.visual_canvas.create_rectangle(timbre_x_accum, app.bar_height - timbres[i],
                                                                   timbre_x_accum + 20, app.bar_height, fill='black')
            pitch_x_accum += 25
            timbre_x_accum += 25

    app.root.after(50, gui_updater, app)


def main():
    # This only needs to be run sometimes?
    # multiprocessing.set_start_method('spawn')
    app = AVisGUI()
    app.root.after(50, gui_updater, app)
    app.start()


if __name__ == "__main__":
    main()
