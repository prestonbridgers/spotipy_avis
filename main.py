import pyaudio
from tkinter import *
from tkinter import ttk


class AVisGUI:
    def __init__(self):
        self.root = Tk()
        self.root.title("Spotipy Audio Visualizer")

        # Create main frame
        self.mainframe = ttk.Frame(self.root, padding="3 3 12 12")
        self.mainframe.grid(column=0, row=0, sticky="N W E S")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Creating entry widget
        self.feet = StringVar() # Create a variable to hold the value
        # Create the actual entry widget inside the main frame
        feet_entry = ttk.Entry(self.mainframe, width=7, textvariable=self.feet)
        feet_entry.grid(column=2, row=1, sticky="W E")

        self.meters = StringVar()
        ttk.Label(self.mainframe, textvariable=self.meters).grid(column=2, row=2, sticky="W E")

        ttk.Button(self.mainframe, text="Calculate", command=self.calculate).grid(column=3, row=3, sticky="W")

        ttk.Label(self.mainframe, text="feet").grid(column=3, row=1, sticky="W")
        ttk.Label(self.mainframe, text="=").grid(column=1, row=2, sticky="E")
        ttk.Label(self.mainframe, text="meters").grid(column=3, row=2, sticky="W")

    def calculate(self, *args):
        try:
            value = float(self.feet.get())
            self.meters.set(str(value))
        except ValueError:
            pass

    def start(self):
        self.root.mainloop()


def main():
    app = AVisGUI()
    app.start()


if __name__ == "__main__":
    main()
