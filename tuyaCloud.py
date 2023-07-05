# Standard library imports
# Home version 22 02 2023
from time import sleep as time_sleep
from os import path
from datetime import datetime
from sys import exit as sys_exit
from operator import itemgetter
import json
import yaml
from utility import prd as debugPrint
from inspect import currentframe as cf
from inspect import getframeinfo as gf
import tinytuya
#from subprocess import callpython -m pip install tinytuya

class class_tuyaCloud:
	def __init__(self,config,tinyTuyaJson):
     
		# Save required data from Config for this class
		self.TD = config.TD
		self.numberCommandDevices = config.data["Tuya"]["numberCommandDevices"]
		self.debug = config.debug		
		self.numConfiguredDevices = len(self.TD)
		
		self.cloud = tinytuya.Cloud(
			apiRegion= tinyTuyaJson["apiRegion"],
			apiKey=tinyTuyaJson["apiKey"],
			apiSecret=tinyTuyaJson["apiSecret"], 
			apiDeviceID=tinyTuyaJson["apiDeviceID"])
		self.devices = self.cloud.getdevices()
		self.numRegisteredDevices = len(self.devices)
		self.properties = [{}]*self.numRegisteredDevices
		if self.numRegisteredDevices > 0 :
			for ind in range(self.numRegisteredDevices):
				self.properties[ind] = self.cloud.getproperties(self.devices[ind]["id"])

		self.commandPairs = [[]] * self.numberCommandDevices

		self.switchOn = [False]*self.numConfiguredDevices

		self.devicesStatus = [{}]*self.numConfiguredDevices

		for device in range(0,self.numConfiguredDevices):
			status = self.cloud.getstatus(self.TD[device]["id"])
			deviceStatus =  {}
			debugPrint(self.debug,f'device number {device}')
			try:
				debugPrint(self.debug,f'status["result"] is {status["result"]}')
			except:
				debugPrint(self.debug,f'\n reached end of devices with readable status at number {device} \n')
				break
			for item in status["result"]:
				deviceStatus[item["code"]] = item["value"]
				if item["code"][:6] == "switch":
					self.switchOn[device] = item["value"]
			self.devicesStatus[device] = deviceStatus

			debugPrint(self.debug,f'self.TD[device]["codes"]): {self.TD[device]["codes"]}   self.TD[device]["values"] : {self.TD[device]["values"]}')
			codesLength = len(self.TD[device]["codes"])
			valuesLength = len(self.TD[device]["values"])
			debugPrint(self.debug,f'For device {device} called {self.TD[device]["name"]} codesLength {codesLength}  valuesLength {valuesLength}')

			# Setup the command pairs for each device This is used to create the commands to
			# send to a device. This is only  done for the first "commandsets" devices
			# and for each device only for the first "command pairs" of codes and values.	
		for device in range(self.numberCommandDevices):
			if len(self.TD[device]["codes"]) != len(self.TD[device]["values"]):
				print(f'Error device {device} called {self.TD[device]["name"]} \
					self.TD[device]["codes"]) and self.TD[device]["values"]) are {self.TD[device]["codes"]} and {self.TD[device]["values"]}')
				sys_exit()
			pairs = []
			for pair in range(self.TD[device]["numCommandPairs"]):
				pairs.append(dict(code = self.TD[device]["codes"][pair],value = self.TD[device]["values"][pair]))
			self.commandPairs[device] = pairs
			debugPrint(self.debug,f'self.commandPairs  {self.commandPairs}')

	def amendCommands(self,device,code,value):
		# The first "command sets" devices each have 
		# "commandpairs" of pairs of commands
		# in this function we look for the "code"
		# in device "device" abd set its value to "value".
		# not it must be the right data type but that type is determined
  
  
     
     
		debugPrint(self.debug,f'Doing Amend Command for device {device} code {code} and value {value}')
		numberCommands = len(self.commandPairs[device])
		result = False
		debugPrint(self.debug,f'numberCommands {numberCommands}  self.commandPairs {self.commandPairs}')
		for commandIndex in range(0,numberCommands):
			debugPrint(self.debug,f'commandIndex {commandIndex}')
			commandCode = self.commandPairs[device][commandIndex]["code"]
			debugPrint(self.debug,f'commandCode {commandCode}')
			if commandCode == code:
				if str(value) == 'True': 
					self.commandPairs[device][commandIndex]["value"] = True
				elif str(value) == 'False':
					self.commandPairs[device][commandIndex]["value"] = False
				else:
					print("Missing or incorrect code type",commandIndex,self.valuesTypes[device],code)
					sys_exit()
				result = True # to signal found code
		return result

	def upDateDevice(self,device):    # sets device to match values in commands

		# Assume online until get bad result and offline confirmed
		reason = ""
		numberCommands =  len(self.commandPairs[device])
		success = [True]*numberCommands
		for commandIndex in range(0,numberCommands):
			commandCode = self.commandPairs[device][commandIndex]["code"]
			statusValue = str(self.devicesStatus[device][commandCode])
			command = self.commandPairs[device][commandIndex]
			commandValue = str(command["value"])
			if (statusValue != commandValue) or (commandIndex == 0):
				# Create the json command to send
				commands = { 'commands' : command}
				try:
					finfo = gf(cf())
					status = self.cloud.sendcommand(self.TD[device]["id"],commands)
					success[commandIndex] = status["success"]
					if status.get('msg','device is online') == 'device is offline':
						reason += self.TD[device]["name"] + "is offLine"
					if not(success[commandIndex]):
						reason += self.TD[device]["name"]+ "/" + commandCode + " cmnd  fail msg: " + status.get('msg','no msg')
						success[commandIndex] = False
						print("send command fail",reason)
				except Exception as err:	
					exc = f' File: {finfo.filename} Ln: {finfo.lineno} Type: {str(type(err))[8:-2]} Error: {str(err)}'
					print(exc)
					reason += exc
					success[commandIndex] = False

		time_sleep(1)

		try:
			finfo = gf(cf())
			status = self.cloud.getstatus(self.TD[device]["id"])
			stSuccess = status["success"]
		except Exception as err:
			exc = f' File: {finfo.filename} Ln: {finfo.lineno} Type: {str(type(err))[8:-2]} Error: {str(err)}'
			print(exc)
			reason += exc
			stSuccess = False
		if stSuccess:
			statusValues = {}
			for item in status["result"]:
				statusValues[item["code"]] = item["value"]
				if item["code"][:6] == "switch":
					self.switchOn[device] = item["value"]
			self.devicesStatus[device] = statusValues
		else:
			reason += " Get Status Fail (result) " + self.TD[device]["name"] + " "
			print("get status fail",reason)
		try:
			finfo = gf(cf())
			if status.get('msg','device is online') == 'device is offline':
				reason += self.TD[device]["name"] + " is offLine"
				print(f'\n\n {self.TD[device]["name"]} is offline')
				stSuccess = False
		except Exception as err:
			exc = f' File: {finfo.filename} Ln: {finfo.lineno} Type: {str(type(err))[8:-2]} Error: {str(err)}'
			print(exc)
			reason += exc

		return success,stSuccess,reason

	def getStatus(self):
		stSuccess = [False]*self.numConfiguredDevices
		status = []
		finfo = gf(cf())
		failReason= [""]
		for number in range(self.numConfiguredDevices):
			failReason.append("")
		for device in range(0,self.numConfiguredDevices):
			try:
				finfo = gf(cf())
				status = self.cloud.getstatus(self.TD[device]["id"])
				stSuccess[device] = status.get('success',False)
			except Exception as err:
				exc =  f' File: {finfo.filename} Ln: {finfo.lineno} Type: {str(type(err))[8:-2]} Error: {str(err)}'
				print(exc)
				failReason[device] += exc
			if stSuccess[device]:
				statusValues = {}
				for item in status["result"]:
					debugPrint(self.debug,f'""Tuyacloud Get Status Results, item["code"]  {item["code"]} item["value"]  {item["value"]}'"")
					if (item["code"] == "switch") or (item["code"] == "switch_1"):
						if str(item["value"]) == "True":
							self.switchOn[device] = True
							statusValues[item["code"]] = True
						elif str(item["value"]) == "False":
							self.switchOn[device] = False
							statusValues[item["code"]] = False
						else:
							print("error TuyaCloud 278  ",item["code"],item["value"])
							sys_exit()
					else:
						statusValues[item["code"]] = item["value"]
				self.devicesStatus[device] = statusValues
			else:
				try:
					finfo = gf(cf())
					debugPrint(self.debug,f'@line 223 try device number = :"{device} called {self.TD[device]["name"]}')
					failReason[device] += " Get Status Fail (result) " + self.TD[device]["name"] + " "
				except Exception as err:
					exc = f' File: {finfo.filename} Ln: {finfo.lineno} Type: {str(type(err))[8:-2]} Error: {str(err)}'
					print(exc)
					failReason[device] += exc
			# problem here was list object "status". "has no get
			try:
				finfo = gf(cf())
				if status.get('msg','device is online') == 'device is offline':
					failReason[device] += self.TD[device]["name"] + " is offLine"
					stSuccess[device] = False
			except Exception as err:
				exc = f' File: {finfo.filename} Ln: {finfo.lineno} Type: {str(type(err))[8:-2]} Error: {str(err)}'
				print(exc)
				failReason[device] += exc
		return stSuccess,failReason,self.devicesStatus


	def listDevices(self):
		# Get list of devices
		devices = self.cloud.getdevices()
		return devices

	def deviceProperties(self,id):
		#Get Properties of Device
		properties = self.cloud.getproperties(id)
		return properties

# test routine un when script run direct
if __name__ == '__main__':
	# change this to suite number of switches.
	# one power switch and one heat pump
	# set up the clas
	import sys
	import os
	from paths import class_paths
	appName = "heat"
	paths = class_paths(appName)
	print(f'Apps at {paths.apps}')
	if paths.pathsOK:
		print("Paths are OK")
	else:
		print(f'Error in paths.yml or paths.py.  EXITING')
		print(paths.message)
		sys_exit()

	sys.path.append(paths.apps)  

	from configYml import class_configYml
	appName = "heat"
	functionName = "boiler"
	config = class_configYml(appName,functionName)
	config.scan_count = 0

	print(f'config.debug is {config.debug}')

	config.TD = config.data["Tuya"]["devices"]
 
	filename = "secreted.yml"
	pathname = paths.config
	with open(os.path.join(pathname,filename), 'r') as ymlFile:
		# Reading from yml file
		secretedData = yaml.safe_load(ymlFile)
		debugPrint(config.debug,f'secretedData is {json.dumps(secretedData,indent = 4)}')
		tinyTuyaDictionary = secretedData["tuya"]
	cloud = class_tuyaCloud(config,tinyTuyaDictionary)

	#sys_exit()
	config.debug = True

	dumpText = ""

	if cloud.numRegisteredDevices > 0:
		if config.debug:
			for ind in range(cloud.numRegisteredDevices):
				with open("dump.txt", 'w') as file:
					file.write( f'\n Registered Device Number: {ind}')
					file.write( f'\n {json.dumps(cloud.devices[ind],indent = 4)}\n')
					file.write( f'Properties for :  {ind}')
					file.write( f'\n {json.dumps(cloud.properties[ind],indent = 4)}\n')
		else:
			print(f"Number of devices registered is {cloud.numRegisteredDevices}")

	sys_exit()

	dHp = config.deviceNumberHp
	dHtrs = config.deviceNumberHeaters
	cloud.amendCommands(dHp,"temp_set",27)


	print("\n set to default")
	success,stSuccess,failreason = cloud.upDateDevice(dHp)
	print("Reason : ",failreason)
	time_sleep(10)

	if cloud.amendCommands(dHp,"switch_1",True):
		print("found  ",code )
	else:
		print("error  ", code)
	print("\n set switch on")
	success,stSuccess,failreason = cloud.upDateDevice(dHp)
	print("Reason : ",failreason)
	time_sleep(10)

	code = "temp_set"
	value = 22
	cloud.amendCommands(dHp,code,value)
	print("\n set temp 22")
	success,stSuccess,failreason = cloud.upDateDevice(dHp)
	print("Reason : ",failreason)

	sys_exit()

	commandPairs[1][0]["value"] = False
	print(commandPairs[1][0]["code"]," set to ",commandPairs[1][0]["value"])
	commandPairs[1][4]["value"] = 25
	print(commandPairs[1][4]["code"]," set to ",commandPairs[1][4]["value"])
	listCodes = []
	for ind in range(0,len(commandPairs[1])):
		listCodes.append(commandPairs[1][ind]["code"] + " is " + str(commandPairs[1][ind]["value"]))
	print(listCodes)

	success,stSuccess,opFail,stOpFail,printMessage,reason = cloud.sendCommands(dHp,commandPairs[1],start,end)
	print(success,stSuccess,opFail,stOpFail,printMessage,reason)

	sys_exit()

	start = 0
	end = 0	
	success,stSuccess,opFail,stOpFail,printMessage,reason = cloud.sendCommands(dHp,commandPairs[1],start,end)
	print(success,stSuccess,opFail,stOpFail,printMessage,reason)

	start = 4
	end = 4
	success,stSuccess,opFail,stOpFail,printMessage,reason = cloud.sendCommands(dHp,commandPairs[1],start,end)
	print(success,stSuccess,opFail,stOpFail,printMessage,reason)
	sys_exit()

	count = 0

	while count < 5  :
		temp, humidity, battery = cloud.getTH(id)
		print(temp,humidity,battery)
		print(datetime.now())
		count += 1
		print(count)
