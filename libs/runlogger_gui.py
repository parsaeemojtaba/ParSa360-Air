import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QRadioButton, QPushButton, QLineEdit

# Import threading and multiprocessing modules
import threading
import multiprocessing

sys.path.insert(1, '/home/pi/ParSa360-Air/libs')
from ParSa360Air_Logger import ParSa360Air_Logger


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ParSa360-Air Logger")
        self.logger = ParSa360Air_Logger()

        layout = QVBoxLayout()

        raspberry_pi_layout = QHBoxLayout()  # Layout for Raspberry Pi selection
        raspberry_pi_label = QLabel("Set Raspberry Pi:")
        raspberry_pi_layout.addWidget(raspberry_pi_label)

        self.raspberry_pi_1 = QRadioButton("1")
        self.raspberry_pi_2 = QRadioButton("2")

        raspberry_pi_layout.addWidget(self.raspberry_pi_1)
        raspberry_pi_layout.addWidget(self.raspberry_pi_2)

        layout.addLayout(raspberry_pi_layout)  # Add Raspberry Pi layout to the main layout

        measurement_duration_label = QLabel("Set the entire duration of measurement in minutes:")
        self.measurement_duration_input = QLineEdit()
        layout.addWidget(measurement_duration_label)
        layout.addWidget(self.measurement_duration_input)

        capture_duration_label = QLabel("Set the duration of each sensory capture in seconds:")
        self.capture_duration_input = QLineEdit()
        layout.addWidget(capture_duration_label)
        layout.addWidget(self.capture_duration_input)

        sensor_sleep_time_label = QLabel("Set the delay between each sensory capture in seconds:")
        self.sensor_sleep_time_input = QLineEdit()
        layout.addWidget(sensor_sleep_time_label)
        layout.addWidget(self.sensor_sleep_time_input)

        hqcamera_sleep_time_label = QLabel("Set the delay between each imagery camera capture in minutes:")
        self.hqcamera_sleep_time_input = QLineEdit()
        layout.addWidget(hqcamera_sleep_time_label)
        layout.addWidget(self.hqcamera_sleep_time_input)

        self.start_button = QPushButton("Start Logging")
        self.start_button.clicked.connect(self.start_logging)
        layout.addWidget(self.start_button)

        cancel_button = QPushButton("Cancel Logging")
        cancel_button.clicked.connect(self.cancel_logging)
        layout.addWidget(cancel_button)

        self.setLayout(layout)

        self.is_logging = False  # Variable to track the logging state

    def start_logging(self):
        if self.is_logging:
            return  # Ignore the button click if already logging

        if self.raspberry_pi_1.isChecked():
            set_raspberry_pi = 1
        else:
            set_raspberry_pi = 2

        measurement_duration = int(self.measurement_duration_input.text())
        capture_duration = int(self.capture_duration_input.text())
        sensor_sleep_time = int(self.sensor_sleep_time_input.text())
        hqcamera_sleep_time = int(self.hqcamera_sleep_time_input.text())

        # Disable the "Start Logging" button
        self.start_button.setEnabled(False)

        # Set the logging state
        self.is_logging = True

        # Start logging in a separate thread
        threading.Thread(target=self.run_logging, args=(set_raspberry_pi, measurement_duration, capture_duration,
                                                        sensor_sleep_time, hqcamera_sleep_time)).start()

    def run_logging(self, set_raspberry_pi, measurement_duration, capture_duration, sensor_sleep_time, hqcamera_sleep_time):
        # Call the logger's main method
        self.logger.main(set_raspberry_pi, measurement_duration, capture_duration,
                         sensor_sleep_time, hqcamera_sleep_time)

        # Re-enable the "Start Logging" button
        self.start_button.setEnabled(True)

        # Reset the logging state
        self.is_logging = False

    def cancel_logging(self):
        # Terminate all threads and processes
        threading.active_count()
        for thread in threading.enumerate():
            if thread is not threading.main_thread():
                thread.join()

        multiprocessing.active_children()
        for process in multiprocessing.active_children():
            process.terminate()

        # Reset the logging state
        self.is_logging = False


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
