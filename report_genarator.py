import os
from datetime import datetime


class ReportGenerator:

    @staticmethod
    def generate_report(bpm_history):

        if len(bpm_history) == 0:
            return

        os.makedirs(
            "output/reports",
            exist_ok=True
        )

        report_file = (
            "output/reports/"
            "heart_rate_report.txt"
        )

        avg_bpm = sum(bpm_history) / len(bpm_history)
        max_bpm = max(bpm_history)
        min_bpm = min(bpm_history)

        with open(
            report_file,
            "w"
        ) as file:

            file.write(
                "Heart Rate Session Report\n"
            )

            file.write(
                "=========================\n\n"
            )

            file.write(
                f"Date: "
                f"{datetime.now()}\n\n"
            )

            file.write(
                f"Average BPM: "
                f"{avg_bpm:.2f}\n"
            )

            file.write(
                f"Maximum BPM: "
                f"{max_bpm}\n"
            )

            file.write(
                f"Minimum BPM: "
                f"{min_bpm}\n"
            )

            file.write(
                f"Total Samples: "
                f"{len(bpm_history)}\n"
            )

        print(
            "\nReport saved to:",
            report_file
        )