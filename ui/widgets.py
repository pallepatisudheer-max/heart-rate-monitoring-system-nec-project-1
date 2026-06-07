import tkinter as tk


class BPMLabel:

    def __init__(self, parent):

        self.label = tk.Label(
            parent,
            text="BPM: --",
            font=("Arial", 24, "bold"),
            fg="red"
        )

        self.label.pack(pady=20)

    def update(self, bpm):

        self.label.config(
            text=f"BPM: {bpm}"
        )