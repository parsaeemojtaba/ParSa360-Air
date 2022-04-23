#!/usr/local/bin/python3

import sys
from multiprocessing import Process
sys.path.append('../')
import ParSaDataLoggerRunWriteFunctions as SensRunWriteFunctions
import ParSaDataLogger_SensorReadFunctionClass as SensReadFunctions
import ParSaDataLoggerGeneralFunctions as generalFunctions
dataloggerMainDir='/home/pi/DataLogger/'
gf=generalFunctions.generalFunctions(dataloggerMainDir)
readSens=SensReadFunctions.readingSensors(gf)  

def dataLog(setRaspberryPi, delay, sleepStep): 
    runClass=SensRunWriteFunctions.runSensors(readSens, gf, delay, sleepStep)
    if setRaspberryPi==1:   
        ####################################### seeed mlx9064x1 thermal cam, AS spectrometer, DFrobot expansion hat and df VEML libs are required
        import AS7265xClass as AS7265x
        import DFRobot_VEML7700 as DFveml
        from DFRobot_RaspberryPi_Expansion_Board import DFRobot_Expansion_Board_IIC as Board_DFRobot
        import seeed_mlx9064x1 as mlx

        ####################################### set folders and file names
        SensorType = 'CO2Level'
        dataLogsPath, sensorsCO2DirPath = gf.makeDataLoggerDir(SensorType)
        sensorCO2FileName='CO2Level'

        SensorType = 'LuxMeters'
        NSensorsLux = 6
        LuxMeter_i2c6Bus = [11, 15, 12, 13, 16, 14]
        dataLogsPath, sensorsLuxDirPath = gf.makeDataLoggerDir(SensorType)
        sensorLuxFilenames = []
        for sensorNum in range (0, NSensorsLux): 
            sensorFileNameX='LuxSens_'+str(sensorNum+1)
            print(sensorFileNameX)
            sensorLuxFilenames.append(sensorFileNameX)

        SensorType = 'ThermalCamSens'
        NSensorsThermCam = 8
        ThermCam_i2c6Bus = [11, 15, 12, 13, 16, 14, 10, 1]
        dataLogsPath, sensorsThermCamDirPath = gf.makeDataLoggerDir(SensorType)
        sensorThermCamStatFilenames = []
        sensorThermCamSceneFilenames = []
        for sensorNum in range (0, NSensorsThermCam): 
            sensorFileNameX='Stats_ThermalCam_'+str(sensorNum+1)
            print(sensorFileNameX)
            sensorThermCamStatFilenames.append(sensorFileNameX)

            sensorFileNameY='Scene_ThermalCam_'+str(sensorNum+1)
            print(sensorFileNameY)
            sensorThermCamSceneFilenames.append(sensorFileNameY)

        SensorType = 'AsSpectrophotometers'
        NSensorsAS = 4
        ASspdMeter_i2c6Bus = [11, 12, 13, 14]
        dataLogsPath, sensorsASspdDirPath = gf.makeDataLoggerDir(SensorType)
        sensorASspdFilenames = []
        for sensorNum in range (0, NSensorsAS): 
            sensorFileNameX='SpdSens_'+str(sensorNum+1)
            print(sensorFileNameX)
            sensorASspdFilenames.append(sensorFileNameX)

        SensorType = 'SoundMeters'
        NSensorsSound = 4
        DFRobotboard = Board_DFRobot(1, 0x10)    # Select i2c bus 1, set address to 0x10
        if DFRobotboard.last_operate_status == DFRobotboard.STA_OK:
            DFRobotboard.set_adc_enable()
            ADCports=[]
            ADCPort_1= DFRobotboard.A3
            ADCports.append(ADCPort_1)
            ADCPort_2= DFRobotboard.A2
            ADCports.append(ADCPort_2)
            ADCPort_3= DFRobotboard.A1
            ADCports.append(ADCPort_3)
            ADCPort_4= DFRobotboard.A0
            ADCports.append(ADCPort_4)
            # print("Df robot board status is detected and adc ports are activated!")
        else:
            print('Df robot board is NOT detected!')

        dataLogsPath, sensorsSoundDirPath = gf.makeDataLoggerDir(SensorType)
        sensorSoundFilenames = []
        for sensorNum in range (0, NSensorsSound): 
            sensorFileNameX='SoundSens_'+str(sensorNum+1)
            print(sensorFileNameX)
            sensorSoundFilenames.append(sensorFileNameX)

        ###############################################################################################################
        ########################################### Run modules #######################################################
        ###############################################################################################################
        argsThermalCamSens=[]
        for sensorNum in range (0, NSensorsThermCam): 
            argsThermalCamSens.append((mlx, ThermCam_i2c6Bus[sensorNum], sensorsThermCamDirPath, 
                                                sensorThermCamStatFilenames[sensorNum], sensorThermCamSceneFilenames[sensorNum]))
        pThermalCamSens_1 = Process(target = runClass.runIrThermalCamSen, args=argsThermalCamSens[0])
        pThermalCamSens_2 = Process(target = runClass.runIrThermalCamSen, args=argsThermalCamSens[1])
        pThermalCamSens_3 = Process(target = runClass.runIrThermalCamSen, args=argsThermalCamSens[2])
        pThermalCamSens_4 = Process(target = runClass.runIrThermalCamSen, args=argsThermalCamSens[3])
        pThermalCamSens_5 = Process(target = runClass.runIrThermalCamSen, args=argsThermalCamSens[4])
        pThermalCamSens_6 = Process(target = runClass.runIrThermalCamSen, args=argsThermalCamSens[5])
        pThermalCamSens_T0 = Process(target = runClass.runIrThermalCamSen, args=argsThermalCamSens[6])
        pThermalCamSens_T1 = Process(target = runClass.runIrThermalCamSen, args=argsThermalCamSens[7])

        argsLuxMetersDF=[]
        for sensorNum in range (0, NSensorsLux): 
            argsLuxMetersDF.append((DFveml, LuxMeter_i2c6Bus[sensorNum], sensorsLuxDirPath, sensorLuxFilenames[sensorNum]))

        pLuxSens_1 = Process(target = runClass.runLuxMeterdf, args=argsLuxMetersDF[0])
        pLuxSens_2 = Process(target = runClass.runLuxMeterdf, args=argsLuxMetersDF[1])
        pLuxSens_3 = Process(target = runClass.runLuxMeterdf, args=argsLuxMetersDF[2])
        pLuxSens_4 = Process(target = runClass.runLuxMeterdf, args=argsLuxMetersDF[3])
        pLuxSens_5 = Process(target = runClass.runLuxMeterdf, args=argsLuxMetersDF[4])
        pLuxSens_6 = Process(target = runClass.runLuxMeterdf, args=argsLuxMetersDF[5])

        argsASspectroMeters=[]
        for sensorNum in range (0, NSensorsAS): 
            argsASspectroMeters.append(( AS7265x, ASspdMeter_i2c6Bus[sensorNum], sensorsASspdDirPath, sensorASspdFilenames[sensorNum]))

        pASspdSens_1 = Process(target = runClass.runASspectroMeter, args=argsASspectroMeters[0])
        pASspdSens_2 = Process(target = runClass.runASspectroMeter, args=argsASspectroMeters[1])
        pASspdSens_3 = Process(target = runClass.runASspectroMeter, args=argsASspectroMeters[2])
        pASspdSens_4 = Process(target = runClass.runASspectroMeter, args=argsASspectroMeters[3])

        argsSoundMetersdf=[]
        for sensorNum in range (0, NSensorsSound): 
            argsSoundMetersdf.append((DFRobotboard, ADCports[sensorNum], sensorsSoundDirPath, sensorSoundFilenames[sensorNum]))

        pSoundSens_1 = Process(target = runClass.runSoundMeterdf, args=argsSoundMetersdf[0])
        pSoundSens_2 = Process(target = runClass.runSoundMeterdf, args=argsSoundMetersdf[1])
        pSoundSens_3 = Process(target = runClass.runSoundMeterdf, args=argsSoundMetersdf[2])
        pSoundSens_4 = Process(target = runClass.runSoundMeterdf, args=argsSoundMetersdf[3])

        pCO2Sens = Process(target = runClass.runCO2, args=(sensorsCO2DirPath, sensorCO2FileName))
        pCO2Sens.start()

        pThermalCamSens_1.start()
        pThermalCamSens_2.start()
        pThermalCamSens_3.start()
        pThermalCamSens_4.start()
        pThermalCamSens_5.start()
        pThermalCamSens_6.start()
        pThermalCamSens_T0.start()
        pThermalCamSens_T1.start()

        pLuxSens_1.start()
        pLuxSens_2.start()
        pLuxSens_3.start()
        pLuxSens_4.start()
        pLuxSens_5.start()
        pLuxSens_6.start()

        pASspdSens_1.start()
        pASspdSens_2.start()
        pASspdSens_3.start()
        pASspdSens_4.start()

        pSoundSens_1.start()
        pSoundSens_2.start()
        pSoundSens_3.start()
        pSoundSens_4.start()


        pCO2Sens.join()

        pThermalCamSens_1.join()
        pThermalCamSens_2.join()
        pThermalCamSens_3.join()
        pThermalCamSens_4.join()
        pThermalCamSens_5.join()
        pThermalCamSens_6.join()
        pThermalCamSens_T0.join()
        pThermalCamSens_T1.join()

        pLuxSens_1.join()
        pLuxSens_2.join()
        pLuxSens_3.join()
        pLuxSens_4.join()
        pLuxSens_5.join()
        pLuxSens_6.join()

        pASspdSens_1.join()
        pASspdSens_2.join()
        pASspdSens_3.join()

        pSoundSens_1.join()
        pSoundSens_2.join()
        pSoundSens_3.join()
        pSoundSens_4.join()


    if setRaspberryPi==2:
        ####################################### if SHT and PM2.5 sensor is attached
        import grove_I2C_High_Accuracy_tem_hum_SHT35_sensor as SHT35
        TempHumSensorSHT = SHT35.GroveTemperatureHumiditySensorSHT3x()

        from adafruit_pm25.uart import PM25_UART
        import serial
        reset_pin = None
        uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=0.25)
        # Connect to a PM2.5 sensor over UART
        pm25 = PM25_UART(uart, reset_pin)

        ####################################### set folders and file names
        SensorType = 'TempHumiditySht'
        dataLogsPath, sensorsTempHumShtDirPath = gf.makeDataLoggerDir(SensorType)
        sensorTempHumShtFileName='TempHumiditySht'

        SensorType = 'Pm25AirQaulity'
        dataLogsPath, sensorsPm25DirPath = gf.makeDataLoggerDir(SensorType)
        sensorPm25FileName='Pm25Level'


        ###############################################################################################################
        ########################################### Run modules #######################################################
        ###############################################################################################################
        pTempHumidSensSht = Process(target = runClass.runTempHumidSHT, args=(TempHumSensorSHT, sensorsTempHumShtDirPath, sensorTempHumShtFileName))
        pPm25Sens = Process(target = runClass.runPm25Meter, args=(pm25, sensorsPm25DirPath, sensorPm25FileName))

        pPm25Sens.start()
        pTempHumidSensSht.start()

        pPm25Sens.join()
        pTempHumidSensSht.join()
