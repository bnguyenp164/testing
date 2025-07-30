import sys
import datetime
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import QTimer
import pyqtgraph as pg

# Use pynvml to get GPU temperature
try:
    from pynvml import nvmlInit, nvmlDeviceGetHandleByIndex, nvmlDeviceGetTemperature, NVML_TEMPERATURE_GPU
    nvmlInit()
    gpu_handle = nvmlDeviceGetHandleByIndex(0)
    def get_gpu_temp():
        return nvmlDeviceGetTemperature(gpu_handle, NVML_TEMPERATURE_GPU)
except Exception as e:
    print("Warning: GPU not found or pynvml not available:", e)
    def get_gpu_temp():
        return 50  # fallback temp if GPU is not detected

class SensorSimulator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sensor Data from GPU Temp")
        self.resize(900, 700)

        self.start_time = datetime.datetime.now()
        self.timestamps = []
        self.data = []

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Temperature Plot
        self.temp_plot = pg.PlotWidget(title="Temperature (°C)")
        self.temp_plot.setYRange(0, 100)
        self.temp_plot.showGrid(x=True, y=True)
        self.temp_plot.setLabel('bottom', 'Time')
        self.temp_curve = self.temp_plot.plot(pen=pg.mkPen('r', width=2), fillLevel=0, brush=(255, 0, 0, 50))
        self.layout.addWidget(self.temp_plot)

        # Humidity Plot
        self.humid_plot = pg.PlotWidget(title="Humidity (%)")
        self.humid_plot.setYRange(0, 100)
        self.humid_plot.showGrid(x=True, y=True)
        self.humid_plot.setLabel('bottom', 'Time')
        self.humid_curve = self.humid_plot.plot(pen=pg.mkPen('b', width=2), fillLevel=0, brush=(0, 0, 255, 50))
        self.layout.addWidget(self.humid_plot)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['Timestamp', 'Temperature (°C)', 'Humidity (%)'])
        self.layout.addWidget(self.table)

        # Stop button
        self.stop_button = QPushButton("Stop")
        self.stop_button.clicked.connect(self.stop_reading)
        self.layout.addWidget(self.stop_button)

        # Timer for updating
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_data)
        self.timer.start(10000)  # 1 second

    def stop_reading(self):
        self.timer.stop()

    def update_data(self):
        now = datetime.datetime.now()
        elapsed = (now - self.start_time).total_seconds()

        temperature = get_gpu_temp()
        humidity = temperature + 20
        timestamp_str = now.strftime("%H:%M:%S")

        self.timestamps.append(now)
        self.data.append({'timestamp': timestamp_str, 'temperature': temperature, 'humidity': humidity})

        self.table.insertRow(self.table.rowCount())
        self.table.setItem(self.table.rowCount()-1, 0, QTableWidgetItem(timestamp_str))
        self.table.setItem(self.table.rowCount()-1, 1, QTableWidgetItem(str(temperature)))
        self.table.setItem(self.table.rowCount()-1, 2, QTableWidgetItem(str(humidity)))

        self.update_graph()

    def update_graph(self):
        if not self.timestamps:
            return

        x_vals = [(ts - self.start_time).total_seconds() for ts in self.timestamps]
        temps = [d['temperature'] for d in self.data]
        humids = [d['humidity'] for d in self.data]

        self.temp_curve.setData(x=x_vals, y=temps)
        self.humid_curve.setData(x=x_vals, y=humids)

        self.temp_plot.setXRange(0, 3600)
        self.humid_plot.setXRange(0, 3600)

        major_ticks = [(i * 600, (self.start_time + datetime.timedelta(seconds=i * 600)).strftime("%H:%M")) for i in range(7)]
        self.temp_plot.getAxis('bottom').setTicks([major_ticks])
        self.humid_plot.getAxis('bottom').setTicks([major_ticks])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SensorSimulator()
    window.show()
    sys.exit(app.exec_())
