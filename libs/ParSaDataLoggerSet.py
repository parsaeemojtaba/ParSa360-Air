#!/usr/local/bin/python3
import time
import sys
import datetime

LIB_PATH = '/home/pi/ParSa360-Air/libs'
sys.path.insert(1, LIB_PATH)

import ParSaDataLoggerRun as Loggers

def get_input(prompt):
    while True:
        try:
            value = int(input(prompt))
            return value
        except ValueError:
            print('Invalid input. Please enter a valid integer.')

def get_input_minutes(prompt):
    while True:
        try:
            value = int(input(prompt))
            return value * 60  # Convert minutes to seconds
        except ValueError:
            print('Invalid input. Please enter a valid integer.')

def format_time(seconds):
    # Convert seconds to a timedelta object
    duration = datetime.timedelta(seconds=seconds)
    
    # Extract days, hours, minutes, and seconds from the timedelta object
    days = duration.days
    hours, remainder = divmod(duration.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    # Format the time components into a string
    time_string = f"{days} days, {hours:02}:{minutes:02}:{seconds:02}"
    return time_string

def main():
    print('Set Raspberry Pi:')
    set_raspberry_pi = get_input('')

    print('Set the duration of measurement in minutes:')
    measurement_duration = get_input_minutes('')
    measurement_end_time = time.time() + measurement_duration
    
    remaining_time = measurement_end_time - time.time()
    remaining_time_string = format_time(remaining_time)
    print('The measurement will end:', remaining_time_string)

    print('\nSet the delay between each run in seconds:')
    capture_duration = get_input('')

    print('Set the sensor sleep time between each capture in seconds:')
    sensor_sleep_time = get_input('')

    num_capture_per_duration = capture_duration // sensor_sleep_time
    print('Based on your input, there will be about %d captures per the given duration.' % num_capture_per_duration)

    try:
        print('Start measurement')
        measurement_count = 0
        while True:
            if time.time() < measurement_end_time:
                try:
                    Loggers.dataLog(set_raspberry_pi, capture_duration, sensor_sleep_time)
                    measurement_count += 1
                except Exception as e:
                    print('Measurement error:', str(e))
            else:
                print('Measurements are done. Total measurements:', measurement_count)
                break
    except KeyboardInterrupt:
        print('Measurements are terminated.')

if __name__ == '__main__':
    main()
