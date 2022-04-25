#!/usr/local/bin/python3

import sys
LibPath='/home/pi/ParSa360'
sys.path.insert(1, LibPath)
import ParSaDataLoggerRun as Loggers

setRaspberryPi=1
print('set the duration of run in seconds:')
delay=int(input())
print('set the delay between each run:')
sleepStep=int(input())
Loggers.dataLog(setRaspberryPi, delay, sleepStep)
