import numpy as np


class BPMCalculator:

    @staticmethod
    def calculate_bpm(signal, fps):
        print("Signal Length =", len(signal))
        if len(signal) < fps * 5:
            return 0

        signal = np.array(signal)

        # Remove DC component
        signal = signal - np.mean(signal)

        # FFT
        fft = np.fft.fft(signal)

        freqs = np.fft.fftfreq(
            len(signal),
            d=1 / fps
        )

        # Positive frequencies only
        positive_freqs = freqs[:len(freqs)//2]

        positive_fft = np.abs(
            fft[:len(fft)//2]
        )

        # Human heart rate range
        valid = np.where(
            (positive_freqs >= 0.8) &
            (positive_freqs <= 3.0)
        )

        if len(valid[0]) == 0:
            return 0

        peak_freq = positive_freqs[
            valid
        ][
            np.argmax(
                positive_fft[valid]
            )
        ]

        bpm = peak_freq * 60

        # Reject unrealistic values
        if bpm < 30 or bpm > 220:
            return 0

        return int(round(bpm))