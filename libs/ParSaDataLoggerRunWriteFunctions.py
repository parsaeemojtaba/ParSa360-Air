#!/usr/local/bin/python3

import time
import datetime
import numpy as np
import itertools
import pandas as pd

# ============================ time frame run classes

class runSensors:
    def __init__(self, readSens, gf, delay, sleepStep):
        self.readSens = readSens
        self.gf=gf
        self.endTime=time.time()+delay
        self.timeFrame = self.getTimeFrame()
        self.sleepStep=sleepStep
        
        self.timeReadloopHeaders = ['year', 'month', 'day', 'hour', 'minute', 'second']
        self.loopHeaders = ['n.r']
        self.AsChannels = ['ch1', 'ch2', 'ch3', 'ch4', 'ch5', 'ch6',
                                'ch7', 'ch8', 'ch9', 'ch10', 'ch11', 'ch12',
                                    'ch13', 'ch14', 'ch15', 'ch16', 'ch17', 'ch18']
        self.headersAsSensor = self.timeReadloopHeaders + self.loopHeaders + self.AsChannels

        self.pm25items = ['pm10.s', 'pm25.s', 'pm100.s', 'pm10.en', 'pm25.en', 'pm100.en',
                            'par.03um', 'par.05um', 'par.10um', 'par.25um', 'par.50um', 'par.100um']
        self.headersPmSensor = self.timeReadloopHeaders + self.loopHeaders + self.pm25items
 
        self.ThermalCamStat = ['min', '10th', '25th', 'mean', 'median', '75th', '90th', 'max', 'std']
        self.headersThermalCamStat = self.timeReadloopHeaders + self.loopHeaders +self.ThermalCamStat 

        self.ThermalCamScene = list(range(0,768))
        self.headersThermalCamScene= self.timeReadloopHeaders + self.loopHeaders +self.ThermalCamScene       

        # self.headersLuxSensor=['year', 'month', 'day', 'hour', 'minute', 'second', 'n.r', 'lux level']
        self.headersLuxSensor = self.timeReadloopHeaders + self.loopHeaders + ['lux level']
        self.headersSoundSensor = self.timeReadloopHeaders + self.loopHeaders + ['Sound level']
        self.headersTempHumSensor = self.timeReadloopHeaders + self.loopHeaders + self.loopHeaders + ['Temp', 'Humidity']
        self.headersCO2Sensor = self.timeReadloopHeaders + self.loopHeaders + ['CO2', 'Temp']

    def getTimeFrame(self):
        date = datetime.datetime.now()
        date_y = date.strftime("%Y")
        date_m = date.strftime("%m")
        date_d = date.strftime("%d")
        date_h = date.strftime("%H")
        date_mi = date.strftime("%M")
        date_s = date.strftime("%S")
        timeFrame = [date_y, date_m, date_d, date_h, date_mi, date_s]
        return timeFrame
    ####################################### run Thermal cameras
    def runIrThermalCamSen(self, mlx, ThermalCam_i2c6Bus, sensorDirPath, saveFileNameStat, saveFileNameScene): 
        readLoop = 0
        readListStats = pd.DataFrame(columns=self.ThermalCamStat)
        readReportStats_ave = []
        
        readListScenes = pd.DataFrame(columns=self.ThermalCamScene)
        readReportScenes_ave = []

        df_Stats_ave = pd.DataFrame(columns=self.headersThermalCamStat)
        df_Scene_ave = pd.DataFrame(columns=self.headersThermalCamScene)

        ThermCam_Sens = mlx.grove_mxl90640(ThermalCam_i2c6Bus)
        ThermCam_Sens.refresh_rate = mlx.RefreshRate.REFRESH_0_5_HZ
        try:
            while True:
                if time.time()<self.endTime:
                    # print(readLoop+1)
                    run , ThermCam_RawData, ThermScene_StatsDict = self.readSens.readThermalIrCam(ThermCam_Sens)
                    # print(run) 
                    if run == 'Pass':
                        readListStats.loc[len(readListStats)]=np.asarray(list(ThermScene_StatsDict.values()))
                        readListScenes.loc[len(readListScenes)]=ThermCam_RawData
                        time.sleep(self.sleepStep)
                    else:
                        time.sleep(self.sleepStep)
                    readLoop=readLoop+1
                else:
                    ##### Average of stats info
                    if not readListStats.empty:
                        try:
                            readListStat_ave = readListStats.mean(axis=0)
                            numReadStat=len(readListStats)
                        except:
                            print('   >>>> error in averaging!')
                            readListStat_ave = "nan"
                            numReadStat="nan"
                    else:
                        print('   >>>> error in averaging!')
                        readListStat_ave = "nan"
                        numReadStat="nan"

                    ##### Average of pixels
                    if not readListScenes.empty:
                        try:
                            readListScene_ave=readListScenes.mean(axis=0)
                            numReadScene=len(readListScenes)
                        except:
                            readListScene_ave = "nan"
                            numReadScene="nan"
                    else:
                        readListScene_ave = "nan"
                        numReadScene="nan"
                    
                    readListStats.loc[len(readListStats)]=readListStat_ave
                    # print('\n', numReadStat, readListStat_ave)
                    readReportStats_ave.append(self.timeFrame)
                    readReportStats_ave.append([numReadStat])
                    readReportStats_ave.append(readListStats.values[-1])
                    readOutputStat = list(itertools.chain.from_iterable(readReportStats_ave))
                    df_Stats_ave.loc[len(df_Stats_ave)]=readOutputStat
                    self.gf.writeDataFile (sensorDirPath, saveFileNameStat, df_Stats_ave, True, self.headersThermalCamStat)

                    readListScenes.loc[len(readListScenes)]=readListScene_ave
                    # print('\n', numReadScene, readListScene_ave)
                    readReportScenes_ave.append(self.timeFrame)
                    readReportScenes_ave.append([numReadScene])
                    readReportScenes_ave.append(readListScenes.values[-1])
                    readOutputScene = list(itertools.chain.from_iterable(readReportScenes_ave))
                    df_Scene_ave.loc[len(df_Stats_ave)]=readOutputScene
                    self.gf.writeDataFile (sensorDirPath, saveFileNameScene, df_Scene_ave, True, self.headersThermalCamScene)
                    break

            runOut='Thermographic measurements are done!'
            print(runOut)
            return runOut
        except:
            runOut='Cannot run!'
            print(runOut)
            return runOut
    ####################################### run PM 2.5 sensor
    def runPm25Meter(self, pm25, sensorDirPath, saveFileName): 
        readLoop = 0
        readList = pd.DataFrame(columns=self.pm25items)
        readReport = []
        df = pd.DataFrame(columns=self.headersPmSensor)
        try:
            while True:
                if time.time()<self.endTime:
                    # print(readLoop+1)
                    run , particles = self.readSens.readPMsensor(pm25)
                    if run == 'Pass':
                        # print(run,'\n  ', luxLevel)
                        readList.loc[len(readList)]=np.asarray(list(particles.values()))
                        time.sleep(self.sleepStep)
                    else:
                        time.sleep(self.sleepStep)
                    readLoop=readLoop+1
                else:
                    if not readList.empty:
                        try:
                            readList_ave = readList.mean(axis=0)
                            numRead=len(readList)
                        except:
                            print('   >>>> error in averaging!')
                            readList_ave = "nan"
                            numRead="nan"
                    else:
                        print('   >>>> error in averaging!')
                        readList_ave = "nan"
                        numRead="nan"
                    
                    readList.loc[len(readList)]=readList_ave
                    # print('\n', numRead, readList_ave)
                    readReport.append(self.timeFrame)
                    readReport.append([numRead])
                    readReport.append(readList.values[-1])
                    readOutput = list(itertools.chain.from_iterable(readReport))
                    df.loc[len(df)]=readOutput
                    self.gf.writeDataFile (sensorDirPath, saveFileName, df, True, self.headersPmSensor)
                    break
            runOut='PM2.5 level measurements are done!'
            print(runOut)
            return runOut
        except:
            runOut='Cannot run!'
            print(runOut)
            return runOut

    ####################################### run AS spectrophotoMeters
    def runASspectroMeter(self, AS7265x, ASspdMeter_i2c6Bus, sensorDirPath, saveFileName, intime=200): 
        readLoop = 0
        readList = pd.DataFrame(columns=self.AsChannels)
        readReport = []
        df = pd.DataFrame(columns=self.headersAsSensor)
        try:
            while True:
                if time.time()<self.endTime:
                    # print(readLoop+1)
                    run , spd = self.readSens.readSpectra (AS7265x, ASspdMeter_i2c6Bus, intime)
                    if run == 'Pass' and self.gf.isNumeric(spd[3])==True and self.gf.isNumeric(spd[12])==True:
                        # print(run,'\n  ', luxLevel)
                        readList.loc[len(readList)]=np.asarray(spd)
                        time.sleep(self.sleepStep)
                    else:
                        time.sleep(self.sleepStep)
                    readLoop=readLoop+1
                else:
                    if not readList.empty:
                        try:
                            readList_ave = readList.mean(axis=0)
                            numRead=len(readList)
                        except:
                            print('   >>>> error in averaging!')
                            readList_ave = "nan"
                            numRead="nan"
                    else:
                        print('   >>>> error in averaging!')
                        readList_ave = "nan"
                        numRead="nan"
                    
                    readList.loc[len(readList)]=readList_ave
                    # print('\n', numRead, readList_ave)
                    readReport.append(self.timeFrame)
                    readReport.append([numRead])
                    readReport.append(readList.values[-1])
                    readOutput = list(itertools.chain.from_iterable(readReport))
                    df.loc[len(df)]=readOutput
                    self.gf.writeDataFile (sensorDirPath, saveFileName, df, True, self.headersAsSensor)
                    break
            runOut='Spectral level measurements are done!'
            print(runOut)
            return runOut
        except:
            runOut='Cannot run!'
            print(runOut)
            return runOut

    ####################################### run lux level meter 
    def runLuxMeterdf(self, DFveml, LuxMeter_i2c6Bus, sensorDirPath, saveFileName):
        readLoop = 0
        readList = []
        readReport = []
        df = pd.DataFrame(columns=self.headersLuxSensor)
        try:
            while True:
                if time.time()<self.endTime:
                    # print(readLoop+1)
                    run , luxLevel = self.readSens.readLuxSensor_Df(DFveml, LuxMeter_i2c6Bus)
                    if run == 'Pass' and self.gf.isNumeric(luxLevel)==True:
                        # print(run,'\n  ', luxLevel)
                        readList.append(luxLevel)
                        time.sleep(self.sleepStep)
                    else:
                        time.sleep(self.sleepStep)
                    readLoop=readLoop+1
                else:
                    if not readList==[]:
                        try:
                            readList_ave = np.nanmean(np.asarray(readList))
                            numRead=len(readList)
                        except:
                            print('   >>>> error in averaging!')
                            readList_ave = "nan"
                            numRead="nan"
                    else:
                        print('   >>>> error in averaging!')
                        readList_ave = "nan"
                        numRead="nan"
                    # print('\n', numRead, readList_ave)
                    readReport.append(self.timeFrame)
                    readReport.append([numRead, readList_ave])
                    readOutput = list(itertools.chain.from_iterable(readReport))
                    df.loc[len(df)]=readOutput
                    self.gf.writeDataFile (sensorDirPath, saveFileName, df, True, self.headersLuxSensor)
                    break
            runOut='Lux level measurements are done!'
            print(runOut)
            return runOut
        except:
            runOut='Cannot run!'
            print(runOut)
            return runOut

    ####################################### run sound level meter 
    def runSoundMeterdf(self, DFRobotboard, adcPort, sensorDirPath, saveFileName):
        readLoop = 0
        readList = []
        readReport = []
        df = pd.DataFrame(columns=self.headersSoundSensor)
        try:
            while True:
                if time.time()<self.endTime:
                    # print(readLoop+1)
                    run , soundLevel = self.readSens.readSoundSensor_Df(DFRobotboard, adcPort) 
                    if run == 'Pass' and self.gf.isNumeric(soundLevel)==True:
                        # print(run,'\n  ', soundLevel)
                        readList.append(soundLevel)
                        time.sleep(self.sleepStep)
                    else:
                        time.sleep(self.sleepStep)
                    readLoop=readLoop+1
                else:
                    if not readList==[]:
                        try:
                            readList_ave = np.nanmean(np.asarray(readList))
                            numRead=len(readList)
                        except:
                            print('   >>>> error in averaging!')
                            readList_ave = "nan"
                            numRead="nan"
                    else:
                        print('   >>>> error in averaging!')
                        readList_ave = "nan"
                        numRead="nan"
                    # print('\n', numRead, readList_ave)
                    readReport.append(self.timeFrame)
                    readReport.append([numRead, readList_ave])
                    readOutput = list(itertools.chain.from_iterable(readReport))
                    df.loc[len(df)]=readOutput
                    self.gf.writeDataFile (sensorDirPath, saveFileName, df, True, self.headersSoundSensor)
                    break
            runOut='Sound level measurements are done!'
            print(runOut)
            return runOut
        except:
            runOut='Cannot run!'
            print(runOut)
            return runOut

    ####################################### AM/DHT temperature and humidity level meter 
    def runTempHumidAmDht(self, TempHumSensorAMDHT, sensorDirPath, saveFileName):
        readLoop = 0
        readList1 = []
        readList2 = []
        readReport = []
        df = pd.DataFrame(columns=self.headersTempHumSensor)
        try:
            while True:
                if time.time()<self.endTime:
                    # print(readLoop+1)
                    run , temperature_c, humidity = self.readSens.readTempHum_AMDHT(TempHumSensorAMDHT)
                    if run == 'Pass' and self.gf.isNumeric(temperature_c)==True and self.gf.isNumeric(humidity)==True:
                        # print(run,'\n  ', temperature_c, humidity)
                        readList1.append(temperature_c)
                        readList2.append(humidity)
                        time.sleep(self.sleepStep)
                    else:
                        time.sleep(self.sleepStep)
                    readLoop=readLoop+1
                else:
                    if not readList1==[]:
                        try:
                            readList1_ave = np.nanmean(np.asarray(readList1))
                            numRead1=len(readList1)
                        except:
                            print('   >>>> error in averaging!')
                            readList1_ave = "nan"
                            numRead1="nan"
                    else:
                        print('   >>>> error in averaging!')
                        readList1_ave = "nan"
                        numRead1="nan"

                    if not readList2==[]:
                        try:
                            readList2_ave = np.nanmean(np.asarray(readList2))
                            numRead2=len(readList2)
                        except:
                            print('   >>>> error in averaging!')
                            readList2_ave = "nan"
                            numRead2="nan"
                    else:
                        print('   >>>> error in averaging!')
                        readList2_ave = "nan"
                        numRead2="nan"
                    # print('\n', numRead1, numRead2, readList1_ave, readList2_ave)
                    readReport.append(self.timeFrame)
                    readReport.append([numRead1, numRead2, readList1_ave, readList2_ave])
                    readOutput = list(itertools.chain.from_iterable(readReport))
                    df.loc[len(df)]=readOutput
                    self.gf.writeDataFile (sensorDirPath, saveFileName, df, True, self.headersTempHumSensor)
                    break
            runOut='Temperature and humidity measurements are done!'
            print(runOut)
            return runOut
        except:
            runOut='Cannot run!'
            print(runOut)
            return runOut

    ####################################### SHT temperature and humidity level meter 
    def runTempHumidSHT(self, TempHumSensorSHT, sensorDirPath, saveFileName):
        readLoop = 0
        readList1 = []
        readList2 = []
        readReport = []
        df = pd.DataFrame(columns=self.headersTempHumSensor)
        try:
            while True:
                if time.time()<self.endTime:
                    # print(readLoop+1)
                    run , temperature_c, humidity = self.readSens.readTempHum_SHT(TempHumSensorSHT)
                    if run == 'Pass' and self.gf.isNumeric(temperature_c)==True and self.gf.isNumeric(humidity)==True:
                        # print(run,'\n  ', temperature_c, humidity)
                        readList1.append(temperature_c)
                        readList2.append(humidity)
                        time.sleep(self.sleepStep)
                    else:
                        time.sleep(self.sleepStep)
                    readLoop=readLoop+1
                else:
                    if not readList1==[]:
                        try:
                            readList1_ave = np.nanmean(np.asarray(readList1))
                            numRead1=len(readList1)
                        except:
                            print('   >>>> error in averaging!')
                            readList1_ave = "nan"
                            numRead1="nan"
                    else:
                        print('   >>>> error in averaging!')
                        readList1_ave = "nan"
                        numRead1="nan"

                    if not readList2==[]:
                        try:
                            readList2_ave = np.nanmean(np.asarray(readList2))
                            numRead2=len(readList2)
                        except:
                            print('   >>>> error in averaging!')
                            readList2_ave = "nan"
                            numRead2="nan"
                    else:
                        print('   >>>> error in averaging!')
                        readList2_ave = "nan"
                        numRead2="nan"
                    # print('\n', numRead1, numRead2, readList1_ave, readList2_ave)
                    readReport.append(self.timeFrame)
                    readReport.append([numRead1, numRead2, readList1_ave, readList2_ave])
                    readOutput = list(itertools.chain.from_iterable(readReport))
                    df.loc[len(df)]=readOutput
                    self.gf.writeDataFile (sensorDirPath, saveFileName, df, True, self.headersTempHumSensor)
                    break
            runOut='Temperature and humidity measurements are done!'
            print(runOut)
            return runOut
        except:
            runOut='Cannot run!'
            print(runOut)
            return runOut

    ####################################### CO2 and Temp level meter 
    def runCO2(self, sensorDirPath, saveFileName):
        readLoop = 0
        readList1 = []
        readList2 = []
        readReport = []
        df = pd.DataFrame(columns=self.headersCO2Sensor)
        try:
            while True:
                if time.time()<self.endTime:
                    # print(readLoop+1)
                    run , CO2Level, temp_co2 = self.readSens.readCO2sensor()
                    if run == 'Pass' and self.gf.isNumeric(CO2Level)==True and self.gf.isNumeric(temp_co2)==True:
                        # print(run,'\n  ', CO2Level, temp_co2)
                        readList1.append(CO2Level)
                        readList2.append(temp_co2)
                        time.sleep(self.sleepStep)
                    else:
                        time.sleep(self.sleepStep)
                    readLoop=readLoop+1
                else:
                    if not readList1==[]:
                        try:
                            readList1_ave = np.nanmean(np.asarray(readList1))
                            numRead=len(readList1)
                        except:
                            print('   >>>> error in averaging!')
                            readList1_ave = "nan"
                            numRead="nan"
                    else:
                        print('   >>>> error in averaging!')
                        readList1_ave = "nan"
                        numRead="nan"

                    if not readList2==[]:
                        try:
                            readList2_ave = np.nanmean(np.asarray(readList2))
                        except:
                            print('   >>>> error in averaging!')
                            readList2_ave = "nan"
                    else:
                        print('   >>>> error in averaging!')
                        readList2_ave = "nan"
                    # print('\n', numRead, readList1_ave, readList2_ave)
                    readReport.append(self.timeFrame)
                    readReport.append([numRead, readList1_ave, readList2_ave])
                    readOutput = list(itertools.chain.from_iterable(readReport))
                    df.loc[len(df)]=readOutput
                    self.gf.writeDataFile (sensorDirPath, saveFileName, df, True, self.headersCO2Sensor)
                    break
            runOut='CO2 level measurements are done!'
            print(runOut)
            return runOut
        except:
            runOut='Cannot run!'
            print(runOut)
            return runOut



