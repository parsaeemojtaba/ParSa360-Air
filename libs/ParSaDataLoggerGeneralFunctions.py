#!/usr/local/bin/python

import subprocess
import os
import numpy as np
import csv
import pandas as pd

# ============================ store data
class generalFunctions:
    def __init__(self, dataloggerMainDir=None):
        if dataloggerMainDir==None:
            mainPath=os.path.abspath(os.getcwd())
            dataLogsPath=os.path.join(mainPath, 'DataLogger')
            if not os.path.exists(dataLogsPath):
                os.mkdir(dataLogsPath)
        else:
            dataLogsPath=dataloggerMainDir
            if not os.path.exists(dataLogsPath):
                os.mkdir(dataLogsPath)
        if os.path.exists(dataLogsPath):
            CmdLine='sudo chmod a+w '+dataLogsPath
            runChmod=subprocess.Popen(CmdLine, shell=True, stderr=subprocess.PIPE, \
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE,  \
                                universal_newlines=False)
            runChmod.stdout.read()
        self.dataLogsPath=dataLogsPath

     ####################################### create folders
    def makeDataLoggerDir(self, SensorType):
        dataLogsPath=self.dataLogsPath
        sensorsDirPath=os.path.join(dataLogsPath, SensorType)
        if not os.path.exists(sensorsDirPath):
            os.mkdir(sensorsDirPath)
        if os.path.exists(sensorsDirPath):
            CmdLine='sudo chmod a+w '+sensorsDirPath
            runChmod=subprocess.Popen(CmdLine, shell=True, stderr=subprocess.PIPE, \
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE,  \
                                universal_newlines=False)
            runChmod.stdout.read()
        return dataLogsPath, sensorsDirPath
    
    ####################################### write files
    def writeDataFile (self, sensorDirPath, saveFileName, sensor_readings, dataFrame=True, headers=None): 
        txtfilename=str(saveFileName)+'.txt'
        txtfile=os.path.join(os.path.abspath(sensorDirPath), txtfilename)
        if not os.path.isfile(txtfile) and not headers==None:
            if dataFrame==True:
                data_header = pd.DataFrame(columns=headers)
                data_header.to_csv(txtfile, index=False,  sep='\t', mode='w')
            else:
                with open(txtfile, mode='w') as sensorReadingFile:
                    sensor_writetxt = csv.writer(sensorReadingFile, delimiter='\t', quoting=csv.QUOTE_MINIMAL)
                    sensor_writetxt.writerow(headers)

        if os.path.isfile(txtfile):
            CmdLine='sudo chmod a+w '+txtfile
            runChmod=subprocess.Popen(CmdLine, shell=True, stderr=subprocess.PIPE, \
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE,  \
                                universal_newlines=False)
            runChmod.stdout.read()
        # the a is for append, if w for write is used then it overwrites the file
        if dataFrame==True:
            sensor_readings.to_csv(txtfile,  header=None, index=False, sep='\t', mode='a')
        else:
            with open(txtfile, mode='a', newline='') as sensorReadingFile:
                sensor_writetxt = csv.writer(sensorReadingFile, delimiter='\t', quoting=csv.QUOTE_MINIMAL)
                sensor_writetxt.writerow(sensor_readings)
        print('files are written')

    ####################################### check if the vlaue is/could be numerical
    def isNumeric(self, value):
        try:
            value=float(value)
            if np.isnan(value)==True:
                return False
            else:
                return True
        except:
            return False
