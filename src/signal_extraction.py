import cv2
import numpy as np


class SignalExtractor:

    @staticmethod
    def extract_green_signal(frame, roi):

        x, y, w, h = roi

        # Prevent ROI from going outside frame
        height, width = frame.shape[:2]

        x = max(0, x)
        y = max(0, y)

        w = min(w, width - x)
        h = min(h, height - y)

        roi_frame = frame[y:y+h, x:x+w]

        if roi_frame.size == 0:
            return None

        # Extract Green Channel
        green_channel = roi_frame[:, :, 1]

        # Reduce noise
        green_channel = cv2.GaussianBlur(
            green_channel,
            (5, 5),
            0
        )

        # Mean intensity
        signal = np.mean(green_channel)

        return float(signal)