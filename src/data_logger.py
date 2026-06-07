import csv
import os
from datetime import datetime


class DataLogger:

    def __init__(self, filename="output/bpm_logs.csv"):

        self.filename = filename

        os.makedirs(
            "output",
            exist_ok=True
        )

        if not os.path.exists(filename):

            with open(
                filename,
                "w",
                newline=""
            ) as file:

                writer = csv.writer(file)

                writer.writerow([
                    "Timestamp",
                    "BPM",
                    "Signal"
                ])

    def log(
        self,
        bpm,
        signal
    ):

        with open(
            self.filename,
            "a",
            newline=""
        ) as file:

            writer = csv.writer(file)

            writer.writerow([
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                bpm,
                round(signal, 3)
            ])