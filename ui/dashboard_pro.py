import tkinter as tk
from PIL import Image, ImageTk
import cv2
import sys
import os
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

from src.camera import Camera
from src.face_detection import FaceDetector
from src.roi_extraction import ROIExtractor
from collections import deque
from src.signal_extraction import SignalExtractor
from src.signal_filter import SignalFilter
from src.bpm_calculation import BPMCalculator


class DashboardPro:

    def __init__(self):
        
        self.camera = None
        self.detector = FaceDetector()
        self.running = False
        self.signal_buffer = deque(maxlen=300)
        self.freq_buffer = deque(maxlen=100)
        self.fps = 30

        self.root = tk.Tk()

        self.root.title(
            "Heart Rate Monitor Dashboard"
        )

        self.root.geometry(
            "1400x1000"
        )

        self.camera_frame = tk.LabelFrame(
            self.root,
            text="Live Camera"
        )

        self.camera_frame.place(
            x=10,
            y=10,
            width=600,
            height=450
        )

        self.camera_label = tk.Label(
            self.camera_frame,
            bg="black"
        )

        self.camera_label.place(
            x=0,
            y=0,
            width=600,
            height=450
        )
        self.bpm_label = tk.Label(
            self.root,
            text="BPM: --",
            font=("Arial", 24, "bold"),
            fg="red"
        )
        self.bpm_label.place(
            x=750,
            y=250,
            width=250,
            height=50,
        )
        self.freq_label = tk.Label(
            self.root,
            text="Freq: -- Hz",
            font=("Arial", 18, "bold"),
            fg="blue",
            bg="yellow"
        )
        self.freq_label.place(
            x=950,
            y=280,
            width=300,
            height=60
        )
        self.status_label = tk.Label(
            self.root,
            text="Status Text",
            font=("Arial", 18, "bold"),
            fg="blue",
            bg="black"
        )
        self.status_label.place(
            
            x=750,
            y=380,
            width=250,
            height=40
        )
        print("status label created")
        print(self.status_label.winfo_x())
        print(self.status_label.winfo_y())
        
        
        #Graph Frame
        self.graph_frame = tk.LabelFrame(
            self.root,
            text="Live Pulse Signal"
        )
        self.graph_frame.place(
            x=620,
            y=350,
            width=650,
            height=300
        )
        self.figure = Figure(
            figsize=(5, 3),
            dpi=100
        )
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(
            self.figure,
            master=self.graph_frame
        )
        #frequency Graph Frame
        self.freq_graph_frame = tk.LabelFrame(
            self.root,
            text="Frequency Trend"
        )
        self.freq_graph_frame.place(
            x=620,
            y=660,
            width=650,
            height=220
        )
        self.freq_figure=Figure(
            figsize=(5, 2),
            dpi=100
        )
        self.freq_ax= self.freq_figure.add_subplot(111)
        self.freq_canvas = FigureCanvasTkAgg(
            self.freq_figure,
            master=self.freq_graph_frame
        )
        self.freq_canvas.get_tk_widget().pack(
        fill="both",
        expand=True
        )
        self.canvas.get_tk_widget().pack(
            fill=tk.BOTH,
            expand=True
        )   
        self.start_btn = tk.Button( 
            self.root,
            text="Start Monitoring",
            command=self.start_monitoring
        )

        self.start_btn.place(
            x=800,
            y=100,
            width=200,
            height=50
        )
        
        self.start_btn = tk.Button(
            self.root,
            text="Start Monitoring",
            command=self.start_monitoring
        )

        self.start_btn.place(
            x=800,
            y=100,
            width=200,
            height=50
        )

        self.stop_btn = tk.Button(
            self.root,
            text="Stop Monitoring",
            command=self.stop_monitoring
        )

        self.stop_btn.place(
            x=800,
            y=180,
            width=200,
            height=50
        )

    def start_monitoring(self):

        if self.running:
            return

        self.running = True
        self.camera = Camera()

        self.update_camera()

    def stop_monitoring(self):

        self.running = False

        if self.camera:
            self.camera.release()
            self.camera = None

    def update_camera(self):

        if not self.running:
            return

        frame = self.camera.get_frame()

        if frame is not None:
            print("Frame Shape =", frame.shape)

            faces = self.detector.detect(frame)

            for face in faces:

                x, y, w, h = face
                cv2.rectangle(
                    frame,
                    (x, y),
                    (x + w, y + h),
                    (0, 255, 0),
                    2
                )

                left_roi, right_roi = (
                    ROIExtractor.get_eye_rois(face)
                )
                left_signal = SignalExtractor.extract_green_signal(frame, left_roi)
                right_signal = SignalExtractor.extract_green_signal(frame,right_roi)
                if(
                    left_signal is not None and
                    right_signal is not None
                ):
                    signal = (
                        left_signal +
                        right_signal
                    ) / 2
                    self.signal_buffer.append(signal)
                    filtered_signal = SignalFilter.normalize(
                        list(self.signal_buffer)
                    )
                    bpm = BPMCalculator.calculate_bpm(
                        filtered_signal,
                        self.fps
                    )
                    if bpm > 0:
                        self.bpm_label.config(
                            text=f"BPM: {bpm}"
                        )         

                        
                        freq = bpm / 60
                        self.freq_buffer.append(freq)
                        print("Frequency =", freq)

                        self.freq_label.config(
                            text=f"Freq: {freq:.2f} Hz"
                        )
                        if bpm < 60:
                            status = "Low"
                            color = "orange"
                        elif bpm <= 100:
                            color = "green"
                            status = "Normal"
                        else:
                            status = "High"
                            color = "red"
                        self.status_label.config(
                            text=f"Status: {status}",
                            fg=color
                        )
                        self.update_frequency_graph()
                        print("Updating graph")
                        self.ax.clear()
                        print("Plotting:",(self.signal_buffer))
                        self.ax.plot(
                            
                            list(self.signal_buffer)
                        )
                        self.ax.set_title(
                            "Live Pulse Signal"
                        )
                        self.ax.grid(True)
                        
                        self.canvas.draw()
                        print("HEART RATE =", bpm)
                    print(
                        "Signal:", signal,
                        "Buffer:", len(self.signal_buffer),
                        "BPM:", bpm
                        
                        
                    )

                lx, ly, lw, lh = left_roi
                rx, ry, rw, rh = right_roi

                cv2.circle(
                    frame,
                    (lx + lw // 2,
                     ly + lh // 2),
                    20,
                    (255, 0, 0),
                    2
                )

                cv2.circle(
                    frame,
                    (rx + rw // 2,
                     ry + rh // 2),
                    20,
                    (255, 0, 0),
                    2
                )

            frame = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2RGB
            )

            image = Image.fromarray(frame)

            image = image.resize(
                (600, 450)
            )

            photo = ImageTk.PhotoImage(
                image=image
            )

            self.camera_label.imgtk = photo
            self.camera_label.configure(
                image=photo
            )

        self.root.after(
            30,
            self.update_camera
        )
    def update_frequency_graph(self):
        self.freq_ax.clear()
        self.freq_ax.plot(
            list(self.freq_buffer)
        )
        self.freq_ax.set_title(
            "Frequency Trend (Hz)"
        
        )
        self.freq_ax.grid(True)
        self.freq_canvas.draw()
        
    def run(self):

        self.root.mainloop()


if __name__ == "__main__":

    app = DashboardPro()
    app.run()