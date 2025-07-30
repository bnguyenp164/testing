import sys
import time
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import QTimer
from pynvml import *

class TempMonitor(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simulated Temp & Moisture Monitor")
        self.setGeometry(300, 300, 300, 150)

        self.cpu_label = QLabel("Simulated CPU Temp: N/A", self)
        self.gpu_label = QLabel("GPU Temp: N/A", self)

        layout = QVBoxLayout()
        layout.addWidget(self.cpu_label)
        layout.addWidget(self.gpu_label)
        self.setLayout(layout)

        # Initialize NVML for GPU info
        try:
            nvmlInit()
            self.handle = nvmlDeviceGetHandleByIndex(0)
        except NVMLError as err:
            self.gpu_label.setText(f"GPU Error: {err}")
            self.handle = None

        # Update every 2 seconds
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_temps)
        self.timer.start(2000)

    def update_temps(self):
        if self.handle:
            try:
                temp = nvmlDeviceGetTemperature(self.handle, NVML_TEMPERATURE_GPU)
                simulated_cpu_temp = temp - 20

                self.gpu_label.setText(f"GPU Temp (Moisture): {temp} %")
                self.cpu_label.setText(f"Simulated CPU Temp (Temperature): {simulated_cpu_temp} °C")
            except NVMLError as err:
                self.gpu_label.setText(f"Read Error: {err}")
                self.cpu_label.setText("Simulated CPU Temp: N/A")

    def closeEvent(self, event):
        try:
            nvmlShutdown()
        except:
            pass
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TempMonitor()
    window.show()
    sys.exit(app.exec_())
