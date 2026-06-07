import os
import matplotlib.pyplot as plt


class GraphPlot:

    def __init__(self):

        plt.ion()

        self.fig, self.ax = plt.subplots()

        self.line, = self.ax.plot(
            [],
            [],
            linewidth=2
        )

        self.ax.set_title(
            "Live Pulse Signal"
        )

        self.ax.set_xlabel(
            "Samples"
        )

        self.ax.set_ylabel(
            "Signal Intensity"
        )

        self.ax.grid(True)

    def update(self, signal):

        if len(signal) < 2:
            return

        self.line.set_xdata(
            range(len(signal))
        )

        self.line.set_ydata(
            signal
        )

        self.ax.relim()

        self.ax.autoscale_view()

        self.fig.canvas.draw()

        self.fig.canvas.flush_events()

    def save_graph(self):

        os.makedirs(
            "output/graphs",
            exist_ok=True
        )

        self.fig.savefig(
            "output/graphs/pulse_graph.png"
        )

        print(
            "Graph saved successfully."
        )