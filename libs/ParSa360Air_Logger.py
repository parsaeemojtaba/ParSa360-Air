#!/usr/local/bin/python3
import time
import sys
import datetime
import numpy as np
import threading

import time
import sys
import datetime
import numpy as np
import threading

LIB_PATH = '/home/pi/ParSa360-Air/libs'
sys.path.insert(1, LIB_PATH)

import ParSaDataLoggerGeneralFunctions as generalFunctions
from RaspiCamera import RaspiCamera
from ParSaDataLoggerSensoryRun import dataLog


class ParSa360Air_Logger:
    def __init__(self, shutter_speed_array=None):
        self.dataloggerMainDir = '/home/pi/DataLogger/'
        gf = generalFunctions.generalFunctions(self.dataloggerMainDir)
        self.capture_store_dir = gf.dataLogsPath
        # self.capture_store_dir = f"{datalogger_main_dir}/DataLogs"
        if shutter_speed_array is None:
            self.shutter_speed_array = np.array([3200, 4800, 6400, 10000, 20000, 40000, 80000, 120000, 160000])
        else:
            self.shutter_speed_array = np.array(shutter_speed_array)

    @staticmethod
    def get_input(prompt):
        while True:
            try:
                value = int(input(prompt))
                return value
            except ValueError:
                print('Invalid input. Please enter a valid integer.')

    @staticmethod
    def get_input_minutes(prompt):
        while True:
            try:
                value = int(input(prompt))
                return value * 60  # Convert minutes to seconds
            except ValueError:
                print('Invalid input. Please enter a valid integer.')

    def format_time(self, seconds):
        # Convert seconds to a timedelta object
        duration = datetime.timedelta(seconds=seconds)
        
        # Extract days, hours, minutes, and seconds from the timedelta object
        days = duration.days
        hours, remainder = divmod(duration.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        # Format the time components into a string
        time_string = f"{days} days, {hours:02}:{minutes:02}:{seconds:02}"
        return time_string

    def imagery_captures(self, hqcamera_sleep_time, measurement_end_time, set_raspberry_pi):
        capture_main_dir_name = 'Captures_Camera_1' if set_raspberry_pi == 1 else 'Captures_Camera_2'
        try:
            print('Start picturing')
            camera_capture_count = 0
            while time.time() < measurement_end_time:
                try:
                    # Perform image capture
                    camRaspi = RaspiCamera(make_timelapse_capture_dir=True, capture_store_dir=self.capture_store_dir, capture_main_dir_name=capture_main_dir_name)
                    capture_pictures = camRaspi.capture_multiple_pictures(3125, 2500, 'Img_', '.jpg', 100, self.shutter_speed_array, 'off', 2.88671875, 1.8359375)
                    camera_capture_count += 1
                except Exception as e:
                    print('Capturing error:', str(e))
                    
                time.sleep(hqcamera_sleep_time)
                    
            print('Camera capturing is done. Total captures:', camera_capture_count)

        except KeyboardInterrupt:
            print('Camera capturing is terminated.')


    def sensory_captures(self, measurement_end_time, set_raspberry_pi, capture_duration, sensor_sleep_time):
        try:
            print('Start measurement')
            measurement_count = 0
            while True:
                if time.time() < measurement_end_time:
                    try:
                        # Perform sensory captures
                        dataLog(set_raspberry_pi, capture_duration, sensor_sleep_time)
                        measurement_count += 1
                    except Exception as e:
                        print('Measurement error:', str(e))
                else:
                    print('Measurements are done. Total measurements:', measurement_count)
                    break
        except KeyboardInterrupt:
            print('Measurements are terminated.')

    def main(self, set_raspberry_pi, measurement_duration, capture_duration, sensor_sleep_time, hqcamera_sleep_time):
        measurement_end_time = time.time() + measurement_duration
        
        remaining_time = measurement_end_time - time.time()
        remaining_time_string = self.format_time(remaining_time)
        print('The measurement will end:', remaining_time_string)

        num_hqcamera_capture_per_duration = measurement_duration // hqcamera_sleep_time
        num_capture_per_duration = capture_duration // sensor_sleep_time
        print('\nBased on your input, there will be about %d imagery captures per the given duration of measurement.' % num_hqcamera_capture_per_duration)
        print('Based on your input, there will be about %d sensory captures per the given duration of capture.' % num_capture_per_duration)

        

        # Create two threads for running imagery_captures and sensory_captures concurrently
        imagery_thread = threading.Thread(target=self.imagery_captures, args=(hqcamera_sleep_time, measurement_end_time, set_raspberry_pi))
        sensory_thread = threading.Thread(target=self.sensory_captures, args=(measurement_end_time, set_raspberry_pi, capture_duration, sensor_sleep_time))

        # Start the threads
        imagery_thread.start()
        sensory_thread.start()

        # Wait for both threads to finish
        imagery_thread.join()
        sensory_thread.join()
