#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This file is part of pwm_fanshim.
# Copyright (C) 2015 Ivmech Mechatronics Ltd. <bilgi@ivmech.com>
#
# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# title           :config.py
# description     :pwm control for Sauna Electric Heater Control
# author          :David Torrens
# start date      :2019 12 12
# version         :0.1
# python_version  :3

# Standard library imports
from configparser import RawConfigParser
from csv import DictReader as csv_DictReader
from csv import DictWriter as csv_DictWriter
from utility import fileExists, prd
#from datetime import datetime
#from shutil import copyfile
#from ftplib import FTP
#from sys import argv as sys_argv
from sys import exit as sys_exit
#import socket
from os import path
from sys import argv as sys_argv

# Third party imports
#from w1thermsensor import W1ThermSensor

# Local application imports
#from utility import pr,make_time_text,send_by_ftp

class class_config:
	def __init__(self,configFileName):
		self.progPath = path.dirname(path.realpath(__file__)) + "/"
		self.progName = str(sys_argv[0][:-3])
		#self.__default_config_filename = "configHp_default.cfg"
		self.logType = "log" # default log type
		defaultConfig = "default_" + configFileName
		
		if fileExists(configFileName):		
			print( "Will use : " ,configFileName)
			try:
				copyfile("old" + defaultConfig,"older" + defaultConfig)
				print("copied ","old" + defaultConfig," to ","older" + defaultConfig )
			except:
				print("noFilecalled: ","old" + defaultConfig," to copy")
			try:
				copyfile(defaultConfig,"old" + defaultConfig)
				print("copied ",defaultConfig," to ","old" + defaultConfig )
			except:
				print("noFilecalled: ",defaultConfig," to copy")
			try:
				copyfile(configFileName,defaultConfig)
				print("copied ", configFileName," to ",defaultConfig)
			except:
				print("noFilecalled: ",configFileName," to copy")
		elif fileExists(defaultConfig): 
			print("Will copy ",defaultConfig," to ",configFileName, " and use that")
			copyfile(defaultConfig,configFileName)
		else:
			print(debug,"No Config File or defaultt filke must exit")
			sys_exit()


		config_read = RawConfigParser()
		config_read.read(configFileName)
		section = "Scan"
		self.scan_delay = float(config_read.get(section, 'scan_delay')) 
		self.max_scans = float(config_read.get(section, 'max_scans'))
		self.mustLog = float(config_read.get(section, 'mustLog'))
		section = "Log"
		self.log_directory = config_read.get(section, 'log_directory')
		self.local_dir_www = config_read.get(section, 'local_dir_www')
		self.log_buffer_flag = config_read.getboolean(section, 'log_buffer_flag')
		self.text_buffer_length  = int(config_read.get(section, 'text_buffer_length'))		
		section = "Schedule"
		self.shedDays =  config_read.get(section, 'shedDays').split(",")
		self.shedOpen =  config_read.get(section, 'shedOpen').split(",")
		self.program0 =  config_read.get(section, 'program0').split(",")
		self.program1 =  config_read.get(section, 'program1').split(",")
		self.program2 =  config_read.get(section, 'program2').split(",")
		self.program3 =  config_read.get(section, 'program3').split(",")
		self.program4 =  config_read.get(section, 'program4').split(",")
		self.program5 =  config_read.get(section, 'program5').split(",")
		self.program6 =  config_read.get(section, 'program6').split(",")
		section = "MeasureAndControl"
		self.hysteresis =  float(config_read.get(section, 'hysteresis'))
		self.sensor4readings =  int(config_read.get(section, 'sensor4readings'))
		self.switchId = config_read.get(section, 'switchId')
		self.hysteresis =  config_read.getfloat(section, 'hysteresis')
		self.headings = config_read.get(section, 'headings').split(",")
		self.sensorRoomTemp =  config_read.getint(section, 'sensorRoomTemp')
		self.sensorOther = config_read.getint(section, 'sensorOther')
		self.sensorOutside = config_read.getint(section, 'sensorOutside')
		self.names = config_read.get(section, 'names').split(",")
		self.ids   = config_read.get(section, 'ids').split(",")
		self.codes0 = config_read.get(section, 'codes0').split(",")
		self.values0 = config_read.get(section, 'values0').split(",")
		self.values0Types = config_read.get(section, 'values0Types').split(",")
		self.codes1 = config_read.get(section, 'codes1').split(",")
		self.values1 = config_read.get(section, 'values1').split(",")
		self.values1Types = config_read.get(section, 'values1Types').split(",")
		self.deviceNumberHeaters = config_read.getint(section, 'deviceNumberHeaters')
		self.deviceNumberHp = config_read.getint(section, 'deviceNumberHp')
		self.deviceNumberTemp1 = config_read.getint(section, 'deviceNumberTemp1')
		self.deviceNumberTemp2 = config_read.getint(section, 'deviceNumberTemp2')
		self.deviceNumberTemp3 = config_read.getint(section, 'deviceNumberTemp3')
		self.deviceNumberTemp4 = config_read.getint(section, 'deviceNumberTemp4')
		self.numberCommandSets = config_read.getint(section, 'numberCommandSets')
		self.doTest = config_read.getboolean(section, 'doTest')
		self.debug = config_read.getboolean(section, 'debug')
#		New method
		#self.tuyaTempSensorDeviceNumbers = config_read.getint(section, 'tuyaTempSensorDeviceNumbers')
		#self.tuyaTempSensorNames = config_read.get(section, 'tuyaTempSensorNames').split(",")
		#self.gotCodes = config_read.get(section,'codes').split("#")
		#prd(debug,"self.gotCodes  ",self.gotCodes)
		#sys_exit()
		#self.codes = [{}]*self.numberDevices
		#self.codes  = []
		#for ind in self.gotCodes:
		#	self.codes.append(setCodes)
		#self.gotValues = config_read.get(section, 'values').split("#")
		#self.values  = []
		#for setValues in self.gotValues:
		#	self.values.append(setValues)
		#self.gotValuesTypes = config_read.get(section, 'valuesTypes').split("#")
		#self.valuesTypes  = []
		#for setValuesTypes in self.gotValuesTypes:
		#	self.valuesTypes.append(setValuesTypes)

		prd(self.debug,"Program Name is : ",self.progName)
		prd(self.debug,"config file is : ",configFileName)
		prd(self.debug,"Default config file is : ",defaultConfig)
		return




		return

#	def write_file(self):
#		here = "config.write_file"
#		config_write = RawConfigParser()
#		section = "Scan"
#		config_write.add_section(section)
#		config_write.set(section, 'scan_delay',self.scan_delay)
#		config_write.set(section, 'max_scans',self.max_scans)
#		config_write.set(section, 'mustLog',self.mustLog)
#		section = "Log"
#		config_write.add_section(section)
#		config_write.set(section, 'log_directory',self.log_directory)
#		config_write.set(section, 'local_dir_www',self.local_dir_www)
#		config_write.set(section, 'log_buffer_flag',self.log_buffer_flag)
#		config_write.set(section, 'text_buffer_length',self.text_buffer_length)	
#		section = "Schedule"	
#		config_write.add_section(section)
#
#		shedDaysAsString  =",".join(map(str,self.program0))
#		config_write.set(section, 'shedDay',shedDaysAsString)
#
#		shedOpenAsString  =",".join(map(str,self.program0))
#		config_write.set(section, 'shedOpen',shedOpenAsString)
#
#		program0AsString  =",".join(map(str,self.program0))
#		config_write.set(section, 'program0',program0AsString)
#		program0AsString  =",".join(map(str,self.program0))
#		config_write.set(section, 'program0',program0AsString)
#		program0AsString  =",".join(map(str,self.program0))
#		config_write.set(section, 'program0',program0AsString)
#		program0AsString  =",".join(map(str,self.program0))
#		config_write.set(section, 'program0',program0AsString)
#		program0AsString  =",".join(map(str,self.program0))
#		config_write.set(section, 'program0',program0AsString)
#		program0AsString  =",".join(map(str,self.program0))
#		config_write.set(section, 'program0',program0AsString)
#		section = "MeasureAndControl"	
#		config_write.add_section(section)
#		config_write.set(section, 'hysteresis',self.hysteresis)		
#		config_write.set(section, 'sensor4readings',self.sensor4readings)
#		config_write.set(section, 'switchId',self.switchId)
#
#		# Writing our configuration file to 'self.config_filename'
#		pr(self.dbug, here, "ready to write new config file with default values: " , self.config_filename)
#		with open(self.config_filename, 'w+') as configfile:
#			config_write.write(configfile)
#		return 0

# Start of items set in config.cfg
#	# Scan
#		self.scan_delay = 10		# delay in seconds between each scan (not incl sensor responce times)
#		self.max_scans = 0			# number of scans to do, set to zero to scan for ever (until type "ctrl C")
#		self.mustLog = 30			# number of minutes minimum between logging
#	# Log
#		self.log_directory = "log/"	# where to store log files
#		self.local_dir_wl2aqww = "/var/www/html" # default value for local web folder
#		self.log_buffer_flag = True	 # whether to generate the csv log file as well as the html text file	
#		self.text_buffer_length = 30	# number of lines in the text buffer in the html file	
#	# Schedule
#		self.shedDays = (2,3)
#		self.shedOpen = (6,17)
#		self.program0 = (0, 6,0)  # Edit Monday Times and temperatures
#		self.program1 = (0, 6,0)  # Edit Tuesday Times and temperatures
#		self.program2 = (0, 7.5,14.25, 8,14.75, 8.5,15.25, 9,15.75, 9.5,16.00, 10,16.25, 10.5,16, 15.5,0)  # Edit Wednesday Times and temperatures
#		self.program3 = (0, 7.5,14.25, 8,14.75, 8.5,15.25, 9,15.75, 9.5,16.00, 10,16.25, 10.5,16, 15.5,0)  # Edit Thursday Times and temperatures
#		self.program4 = (0, 6,0)  # Edit Friday Times and temperatures
#		self.program5 = (0, 6,0)  # Edit Saturday Times and temperatures
#		self.program6 = (0, 6,0)  # Edit Sunday Times and temperatures
#	# MeasureAndControl
#		self.hysteresis = 0.5
#		self.sensor4readings = 1
#		self.switchId = "bf5723e4b65de4a64fteqz"
#		
## End of items set in config.cfg	
#
## Start of parameters are not saved to the config file
	#	# Based on the program name work out names for other files
#		# First three use the program pathname	
#		self.prog_path = path.dirname(path.realpath(__file__)) + "/"
#		self.prog_name = str(sys_argv[0][:-3])
#		self.config_filename = configFilename
#		self.logType = "log" # default log type
#		print("Program Name is : ",self.prog_name)
#		print("config file is : ",self.config_filename)

#	def read_file(self):
