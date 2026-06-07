import cv2

class Camera:

    def __init__(self):
        self.cap = cv2.VideoCapture(0)

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 700)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 550)

    def get_frame(self):

        ret, frame = self.cap.read()

        if not ret:
            return None

        frame = cv2.resize(
            frame,
            (700, 550)
        )

        return frame

    def release(self):

        self.cap.release()