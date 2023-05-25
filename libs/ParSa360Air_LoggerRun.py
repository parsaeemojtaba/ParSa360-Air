#!/usr/local/bin/python3
import sys
LIB_PATH = '/home/pi/ParSa360-Air/libs'
sys.path.insert(1, LIB_PATH)
from ParSa360Air_Logger import ParSa360Air_Logger

def main():
    # datalogger_main_dir = '/home/pi/DataLogger/'
    data_logger = ParSa360Air_Logger()
    set_raspberry_pi = data_logger.get_input('Set Raspberry Pi:')
    measurement_duration = data_logger.get_input_minutes('Set the entire duration of measurement in minutes:')
    capture_duration = data_logger.get_input('Set the duration of each sensory capture in seconds:')
    sensor_sleep_time = data_logger.get_input('Set the delay between each sensory capture in seconds:')
    hqcamera_sleep_time = data_logger.get_input_minutes('Set the delay between each imagery camera capture in minutes:')
    data_logger.main(set_raspberry_pi, measurement_duration, capture_duration, sensor_sleep_time, hqcamera_sleep_time)

if __name__ == '__main__':
    main()
