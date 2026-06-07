import numpy as np


class SignalFilter:

    @staticmethod
    def moving_average(signal, window_size=5):

        if len(signal) < window_size:
            return np.array(signal)

        filtered = np.convolve(
            signal,
            np.ones(window_size) / window_size,
            mode="valid"
        )

        return filtered

    @staticmethod
    def normalize(signal):

        signal = np.array(signal)

        if len(signal) == 0:
            return signal

        mean = np.mean(signal)
        std = np.std(signal)

        if std == 0:
            return signal

        normalized = (
            signal - mean
        ) / std

        return normalized