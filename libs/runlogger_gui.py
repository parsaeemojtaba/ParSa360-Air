import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QRadioButton, QPushButton, QLineEdit

# Import multiprocessing module
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

        self.logging_process = None  # Process to run the logging process

    def start_logging(self):
        if self.logging_process is not None and self.logging_process.is_alive():
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

        # Create and start a new process for the logging process
        self.logging_process = multiprocessing.Process(
            target=self.run_logging,
            args=(set_raspberry_pi, measurement_duration, capture_duration,
                  sensor_sleep_time, hqcamera_sleep_time)
        )
        self.logging_process.start()

    def run_logging(self, set_raspberry_pi, measurement_duration, capture_duration, sensor_sleep_time, hqcamera_sleep_time):
        # Call the logger's main method in a loop until the logging process is terminated
        while True:
            self.logger.main(set_raspberry_pi, measurement_duration, capture_duration,
                             sensor_sleep_time, hqcamera_sleep_time)

    def cancel_logging(self):
        if self.logging_process is not None and self.logging_process.is_alive():
            self.logging_process.terminate()  # Terminate the logging process
            self.logging_process.join()  # Wait for the logging process to finish

        # Re-enable the "Start Logging" button
        self.start_button.setEnabled(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
