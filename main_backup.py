import cv2
import time
from collections import deque

from config import FACE_BOX_COLOR
from config import THICKNESS

from src.camera import Camera
from src.face_detection import FaceDetector
from src.roi_extraction import ROIExtractor
from src.signal_extraction import SignalExtractor
from src.signal_filter import SignalFilter
from src.bpm_calculation import BPMCalculator
from src.graph_plot import GraphPlot
from src.data_logger import DataLogger
from src.report_generator import ReportGenerator

def main():

    camera = Camera()
    detector = FaceDetector()

    graph = GraphPlot()
    logger = DataLogger()

    signal_buffer = deque(maxlen=300)
    bpm_history = []

    fps = 30
    last_log_time = 0

    while True:

        frame = camera.get_frame()

        if frame is None:
            break

        faces = detector.detect(frame)

        for face in faces:

            x, y, w, h = face

            # Face Rectangle
            cv2.rectangle(
                frame,
                (x, y),
                (x + w, y + h),
                FACE_BOX_COLOR,
                THICKNESS
            )

            # Eye ROIs
            left_roi, right_roi = ROIExtractor.get_eye_rois(face)
            print("Left ROI:", left_roi)
            print("Right ROI:", right_roi)

            lx, ly, lw, lh = left_roi
            rx, ry, rw, rh = right_roi

            # Left Eye Circle
            cv2.circle(
                frame,
                (lx + lw // 2, ly + lh // 2),
                20,
                (255, 0, 0),
                2
            )

            # Right Eye Circle
            cv2.circle(
                frame,
                (rx + rw // 2, ry + rh // 2),
                20,
                (255, 0, 0),
                2
            )

            # Extract Signal From Both Eyes
            left_signal = SignalExtractor.extract_green_signal(
                frame,
                left_roi
            )

            right_signal = SignalExtractor.extract_green_signal(
                frame,
                right_roi
            )

            if left_signal is not None and right_signal is not None:

                signal = (
                    left_signal + right_signal
                ) / 2

                signal_buffer.append(signal)
                print("Signal:", signal)

     
                

                filtered_signal = SignalFilter.moving_average(
                    list(signal_buffer)
                )
                graph.update(
                    filtered_signal
                )
                filtered_signal = SignalFilter.normalize(
                    filtered_signal
                )

                bpm = BPMCalculator.calculate_bpm(
                    filtered_signal,
                    fps
                )

                if bpm > 0:
                    bpm_history.append(bpm)

                current_time = time.time()

                if current_time - last_log_time >= 1:

                    logger.log(
                        bpm,
                        signal
                    )

                    last_log_time = current_time

                cv2.putText(
                    frame,
                    f"BPM: {bpm}",
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 0, 255),
                    2
                )

        cv2.imshow(
            "Heart Rate Measurement",
            frame
        )

        key = cv2.waitKey(1)

        if key == 27:  # ESC
            break

    ReportGenerator.generate_report(
        bpm_history
    )
    graph.save_graph()
    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()