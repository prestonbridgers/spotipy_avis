from gui import AVisGUI
from music_player import song_place


def get_color(num):
    if num == 0:
        return 'red'
    elif num == 1:
        return 'blue'
    elif num == 2:
        return 'green'
    elif num == 3:
        return 'pink'
    else:
        return 'pink'

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

        current_beat = None
        prev_beat = app.data['beats'][0]
        beat_color = 0
        for i, beat in enumerate(app.data['beats']):
            if prev_beat['start'] <= current_time < beat['start']:
                current_beat = prev_beat
                beat_color = i % 4
                break
            else:
                prev_beat = beat
        if current_beat is not None:
            app.visual_canvas.itemconfigure(app.canvas_beatlbl, text=f'Beat {i} Start: {current_beat["start"]}')

        current_bar = None
        prev_bar = app.data['bars'][0]
        bar_color = 0
        for i, bar in enumerate(app.data['bars']):
            if prev_bar['start'] <= current_time < bar['start']:
                current_bar = prev_bar
                bar_color = i % 4
                break
            else:
                prev_bar = bar
        if current_bar is not None:
            app.visual_canvas.itemconfigure(app.canvas_barlbl, text=f'Bar {i} Start: {current_bar["start"]}')

        current_section = None
        prev_section = app.data['sections'][0]
        for i, section in enumerate(app.data['sections']):
            if prev_section['start'] <= current_time < section['start']:
                current_section = prev_section
                break
            else:
                prev_section = section
        if current_section is not None:
            app.visual_canvas.itemconfigure(app.canvas_sectionlbl, text=f'Section {i} Start: {current_section["start"]}')

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
                                                                  pitch_x_accum + 20, app.bar_height, fill=get_color(beat_color))
            app.timbrebars[i] = app.visual_canvas.create_rectangle(timbre_x_accum, app.bar_height - timbres[i],
                                                                   timbre_x_accum + 20, app.bar_height, fill=get_color(bar_color))
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
