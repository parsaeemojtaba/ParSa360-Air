#!/usr/local/bin/python3

import sys
LibPath='/home/pi/ParSa360/libs'
sys.path.insert(1, LibPath)
import ParSaDataLoggerRun as Loggers

print('set Raspberry Pi:')
setRaspberryPi=int(input())
print('set the duration of run in seconds:')
delay=int(input())
print('set the delay between each run:')
sleepStep=int(input())
Loggers.dataLog(setRaspberryPi, delay, sleepStep)
