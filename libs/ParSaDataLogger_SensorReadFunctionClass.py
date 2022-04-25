#!/usr/local/bin/python3

import subprocess
import shlex
import numpy as np

# ============================ class of reading raw data of different sensors
class readingSensors:
    def __init__(self, gf):
        self.gf=gf

    def readSpectra (self, AS7265x, i2cBus, intime=200):
        # reading SparkFun Triad Spectroscopy Sensor - AS7265x
        print('\nreading spectrometer sensor...')
        try:
            Sensor=AS7265x.AS7265x(i2cBus)
            Sensor.setBlueLED(False)
            Sensor.shutterLED("AS72651", False)
            Sensor.shutterLED("AS72652", False)
            Sensor.shutterLED("AS72653", False)
            Sensor.setGain(0)
            Sensor.setIntegrationTime(intime)
            ASspd=Sensor.readCAL()
            #Sensor.readRAW()
            run='Pass'
            # print('sensor '+str(SensorNum)+':\n',Sensorspd,'\n')
        except:
            print('       >>>> error in reading spectral sensor')
            run='Failed'
            ASspd="nan"
        return run, ASspd

    def readSoundSensor_Df (self, DFRobotboard, adcPort):
        print('\nreading sound level meter sensor...')
        # reading Gravity Sound level meter V1.c
        try:
            valueMV=DFRobotboard.get_adc_value(adcPort)
            soundLevel=float((valueMV*50)/1000)
            run='Pass'
        except:
            print('       >>>> error in detecting board')
            run='Failed'
            soundLevel="nan"
            pass
        return run , soundLevel
            
    def readLuxSensor_Df (self, DFveml, i2cBus):
        # reading VEML7700 sensor based on DFRobot_VEML7700
        print('\nreading Lux level meter...')
        try:
            luxSensor=DFveml.DFRobot_VEML7700_I2C(bus_num = i2cBus)
            luxSensor.get_white_lux()
            luxLevel=float(luxSensor.get_ALS_lux())
            run='Pass'
        except:
            print('       >>>> error in reading Lux sensor')
            run='Failed'
            luxLevel="nan"
            pass
        return run , luxLevel
           
    def readCO2sensor(self):
        # reading mhz_19 sensor 
        print('\nreading CO2 sensor...')
        try:
            Co2SensorRaw=subprocess.Popen(['sudo python3 -m mh_z19 --all'], shell=True, stdout=subprocess.PIPE, universal_newlines=True)
            Co2Sensor=Co2SensorRaw.communicate()[0]
            # if not Co2Sensor=='9\n':
            try:
                iaq = shlex.split(Co2Sensor)
                CO2Level=float(iaq[1][:-1])
                temp_co2=float(iaq[3][:-1])
            # print(CO2, temp_co2)
                run='Pass'
            except:
                run='Failed'
                CO2Level="nan"
                temp_co2="nan"
        except:
            print('       >>>> error in reading CO2 sensor')
            run='Failed'
            CO2Level="nan"
            temp_co2="nan"
            pass
        return run, CO2Level, temp_co2

    def readTempHum_AMDHT(self, TempHumSensor):
        # reading DHT22/AM2302 sensor
        print('\nreading temperature and humidity from AM/DHT sensor...')
        try:
            temperature_c = float(TempHumSensor.temperature)
            humidity = float(TempHumSensor.humidity)
            run='Pass'
        except:
            print('       >>>> error in reading temperature and humidity sensor')
            run='Failed'
            temperature_c= "nan"
            humidity= "nan"
            pass
        return run, temperature_c, humidity

    def readTempHum_SHT(self, SHT3X):
        # reading SHT31 sensor
        print('\nreading temperature and humidity from SHT sensor...')
        try:
            SHT3X.begin(RST = 4)
            if (SHT3X.soft_reset() == True):
                temperature_c = float(SHT3X.get_temperature_C())
                humidity = float(SHT3X.get_humidity_RH())
                run='Pass'
            else:
                run='Failed'
        except:
            print('       >>>> error in reading temperature and humidity sensor')
            run='Failed'
            temperature_c="nan"
            humidity="nan"
            pass
        return run, temperature_c, humidity

    def readPMsensor(self, pm25):
        # reading PM 2.5 sensor
        print('\nreading PM 2.5 sensor...')
        try:
            PM25data = pm25.read()
            run='Pass'
        except:
            print("       >>>> error in reading PM25 sensor")
            run='Failed'
            PM25data="nan"
        return run, PM25data

    def readThermalIrCam(self, ThermCam_Sens):
        print('\nreading IR Thermal Camera sensor...')
        try:
            ThermCam_RawData=[0]*768
            ThermCam_Sens.getFrame(ThermCam_RawData) # read MLX temperatures into frame var
            # print(ThermCam_RawData)

            ############### mlx sensors get error very often ########################################################################
            ############### The following loops are to make sure that the measurements are reliable #################################
            if len(ThermCam_RawData) < 769 :
#             print('-- Length pass!')
                if np.isnan(ThermCam_RawData).any()==True:
                    run='Failed'
                    ThermCam_RawData='nan'
                    ThermScene_StatsDict='nan'
                else:
                    for i in range (0, len(ThermCam_RawData)):
                        if self.gf.isNumeric(ThermCam_RawData[i])==True:
                            ThermCam_RawData[i]=float(ThermCam_RawData[i])
                            run='Pass'
                        else:
                            run='Failed'
                            ThermCam_RawData='nan'
                            ThermScene_StatsDict='nan'
                            break

                if run=='Pass':
                    ############### get statistical info ###########################################################################
                    try: 
                        data_90th = np.around(np.percentile(ThermCam_RawData, 90),2)
                        data_75th = np.around(np.percentile(ThermCam_RawData, 75),2)
                        data_25th = np.around(np.percentile(ThermCam_RawData, 25),2)
                        data_10th = np.around(np.percentile(ThermCam_RawData, 10),2)
                        data_std = np.around(np.std(ThermCam_RawData),2)
                        data_mean = np.around(np.mean(ThermCam_RawData),2)
                        data_median = np.around(np.median(ThermCam_RawData),2)
                        data_max = np.around(np.max(ThermCam_RawData),2)
                        data_min = np.around(np.min(ThermCam_RawData),2)
                        ThermScene_StatsDict=dict(  vmin=data_min, 
                                                    v10th=data_10th, 
                                                    v25th=data_25th, 
                                                    vmean=data_mean, 
                                                    vmedian=data_median,  
                                                    v75th=data_75th, 
                                                    v90th=data_90th, 
                                                    vmax=data_max,
                                                    vstd=data_std   )

                        if self.gf.isNumeric(data_max)==False or \
                            self.gf.isNumeric(data_min)==False or \
                            self.gf.isNumeric(data_median)==False or \
                            self.gf.isNumeric(data_mean)==False or \
                            self.gf.isNumeric(data_std)==False or \
                            self.gf.isNumeric(data_25th)==False or \
                            self.gf.isNumeric(data_75th)==False or \
                            self.gf.isNumeric(data_10th)==False or \
                            self.gf.isNumeric(data_90th)==False:
                            print('>>>>>>>>>>> \nThe captured thermal Camera data does not make sense!!!\n')
                            run='Failed'
                            ThermCam_RawData='nan'
                            ThermScene_StatsDict='nan'

                        elif abs(data_max-data_min)>100:
                            print('>>>>>>>>>>> \nThe captured thermal Camera data does not make sense!!!\n')
                            run='Failed'
                            ThermCam_RawData='nan'
                            ThermScene_StatsDict='nan'

                        else:
                            run='Pass'
                    except:
                        run='Failed'
                        ThermCam_RawData='nan'
                        ThermScene_StatsDict='nan'

            else:
                run='Failed'
                ThermCam_RawData='nan'
                ThermScene_StatsDict='nan'
            
        except:
            print("       >>>> error in reading IR Thermal Camera sensor")
            run='Failed'
            ThermCam_RawData='nan'
            ThermScene_StatsDict='nan'

                   
        return run, ThermCam_RawData, ThermScene_StatsDict
