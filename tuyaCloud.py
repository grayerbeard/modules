# Standard library imports
# Home version 22 02 2023
from time import sleep as time_sleep
from os import path
from datetime import datetime
from sys import exit as sys_exit
from operator import itemgetter
import json
from config import class_config
from utility import prd as debugPrint
from inspect import currentframe as cf
from inspect import getframeinfo as gf
#from subprocess import callpython -m pip install tinytuya
		
import tinytuya

class class_tuyaCloud:
	def __init__(self,config,tinyTuyaJson):
		self.numberDevices = len(config.names)
		self.numberCommandSets = config.numberCommandSets
		self.cloud = tinytuya.Cloud(
			apiRegion= tinyTuyaJson["apiRegion"],
			apiKey=tinyTuyaJson["apiKey"],
			apiSecret=tinyTuyaJson["apiSecret"], 
			apiDeviceID=tinyTuyaJson["apiDeviceID"])
        	
		#self.cloud = tinytuya.Cloud()  # uses tinytuya.json 
		self.devices = self.cloud.getdevices()
		self.numDevices = len(self.devices)
		#self.testString = teststring
		
		#self.propertiedebug = Falses = [self.tcloud.getproperties(self.devices[0]['id'])]
		self.properties = [{}]*self.numDevices
		if self.numDevices > 0 :
			for ind in range(self.numDevices):
				self.properties[ind] = self.cloud.getproperties(self.devices[ind]['id'])

		self.ids = config.ids
		self.names = config.names
		self.debug = config.debug
		debug = self.debug

		if(len(self.ids) != self.numberDevices) or \
			(len(self.names) != self.numberDevices) or \
			(len(self.names) != self.numberDevices):
			print("Error TuyaCloud line 46 lengths")
			print(len(self.ids),self.numberDevices,":",len(self.names),self.numberDevices, \
				len(self.names),":",self.numberDevices,int(self.values[device][ind]))
			sys_exit()

		self.commandPairs = [[]]*config.numberCommandSets

		# Get Codes Start Values and Types 
		self.codes = []
		self.codes.append(config.codes0)
		self.codes.append(config.codes1)
		self.codes.append(config.codes2)
		self.codes.append(config.codes3)
		self.codes.append(config.codes4)
		self.codes.append(config.codes5)
		self.codes.append(config.codes6)
		self.codes.append(config.codes7)
		self.codes.append(config.codes8)
		self.codes.append(config.codes9)

		self.values = []
		self.values.append(config.values0)
		self.values.append(config.values1)
		self.values.append(config.values2)
		self.values.append(config.values3)
		self.values.append(config.values4)
		self.values.append(config.values5)
		self.values.append(config.values6)
		self.values.append(config.values7)
		self.values.append(config.values8)
		self.values.append(config.values9)

		self.valuesTypes = []
		self.valuesTypes.append(config.values0Types)
		self.valuesTypes.append(config.values1Types)
		self.valuesTypes.append(config.values2Types)
		self.valuesTypes.append(config.values3Types)
		self.valuesTypes.append(config.values4Types)
		self.valuesTypes.append(config.values5Types)
		self.valuesTypes.append(config.values6Types)
		self.valuesTypes.append(config.values7Types)
		self.valuesTypes.append(config.values8Types)
		self.valuesTypes.append(config.values9Types)

		debugPrint(debug,"Codes: ",self.codes)
		debugPrint(debug,"values: ",self.values)
		debugPrint(debug,"ValueTypes: ",self.valuesTypes)

		#Following line for when checking read in of codes,values and types
		#sys_exit()

		self.switchOn = [False]*self.numberDevices

		self.devicesStatus = [{}]*self.numberDevices
		
		numcommandPairs = [1]*self.numberCommandSets

		for device in range(0,self.numberDevices):
			status = self.cloud.getstatus(self.ids[device])
			deviceStatus =  {}
			for item in status['result']:
				deviceStatus[item["code"]] = item["value"]	
				if item["code"][:6] == "switch":
					self.switchOn[device] = item["value"]
			self.devicesStatus[device] = deviceStatus

			codesLength = len(self.codes[device])
			valuesLength = len(self.values[device])
			debugPrint(debug,f"codesLength {codesLength}  valuesLength {valuesLength}")
			debugPrint(debug,f"codes length and values Length for device : {device} {codesLength}  {valuesLength}")

		for device in range(self.numberCommandSets):
			#self.commandPairs.append([])
			codesLength = len(self.codes[device])
			valuesLength = len(self.values[device])
			numcommandPairs[device] = codesLength
			if codesLength > valuesLength:
				debugPrint(debug,"Less codes than values so only {valuesLength} command pairs will be made")
				numcommandPairs[device] = valuesLength
			elif codesLength < valuesLength:
				debugPrint(debug,"Error with device command pairs : ","")
				debugPrint(debug,"device : ",device)
				debugPrint(debug,"codesLength : ",codesLength," codes : ",self.codes[device])
				debugPrint(debug,"codesLength : ",codesLength," values : ",self.values[device])
				sys_exit()

			debugPrint(debug,self.codes,"\n",self.valuesTypes)
			debugPrint(debug,"Command Pairs: ",self.commandPairs[device])
			debugPrint(debug,"length self.codes",len(self.codes[device]))
			self.commandPairs[device] = []*numcommandPairs[device]
			for ind  in range(numcommandPairs[device]):
				debugPrint(debug,f"Line 121 in Tuyacloud,  ind is {ind} and len(self.codes[device] is {len(self.codes[device])}  self.values {self.values}  self.codes {self.codes}")
				debugPrint(debug,"Device: ",device," Ind: ",ind)
				if str(self.values[device][ind]) == 'True':
					self.commandPairs[device].append(dict(code = self.codes[device][ind],value = True))
				elif str(self.values[device][ind]) == 'False':
					debugPrint(debug,"self.commandPairs[device] ",self.commandPairs[device])
					debugPrint(debug,"self.codes[device] ",self.codes[device])
					debugPrint(debug,"self.codes[device][ind] ",self.codes[device][ind])
					self.commandPairs[device].append(dict(code = self.codes[device][ind],value = False))
					debugPrint(debug,"###self.commandPairs[device] ",self.commandPairs[device])
				elif self.valuesTypes[device][ind] == "s":
					self.commandPairs[device].append(dict(code = self.codes[device][ind],value = str(self.values[device][ind])))
				elif self.valuesTypes[device][ind] == "i":
					self.commandPairs[device].append(dict(code = self.codes[device][ind],value = int(self.values[device][ind])))
				else:
					print(f"Missing or incorrect code type Value Types: {self.valuesTypes[device]} Codes : {self.codes[device]}")
					sys_exit()
		debugPrint(debug,"\n \n Command Pairs\n",self.commandPairs),"\n"
		debugPrint(debug,"\n \n Command Pairs\n",json.dumps(self.commandPairs,indent = 4),"\n")
		for device in range(len(numcommandPairs)):
			for ind  in range(numcommandPairs[device]):
				debugPrint(debug,f"Command Pairs for device {device} are {self.commandPairs[device][ind]}")	
				debugPrint(debug,"\nInitial status \n",json.dumps(self.devicesStatus,indent = 4))

	def amendCommands(self,device,code,value):
		debugPrint(self.debug,f"Doing Amend Command for device {device} code {code} and value {value}")
		numberCommands = len(self.commandPairs[device])
		result = False
		debugPrint(self.debug,f"numberCommands {numberCommands}  self.commandPairs {self.commandPairs}")
		for commandIndex in range(0,numberCommands):
			debugPrint(self.debug,f"commandIndex {commandIndex}")
			commandCode = self.commandPairs[device][commandIndex]["code"]
			debugPrint(self.debug,f"commandCode {commandCode}")
			if commandCode == code:
				if str(value) == 'True': 
					self.commandPairs[device][commandIndex]["value"] = True
				elif str(value) == 'False':
					self.commandPairs[device][commandIndex]["value"] = False
				elif self.valuesTypes[device][commandIndex] == "s": 
					self.commandPairs[device][commandIndex]["value"] = str(value)
				elif self.valuesTypes[device][commandIndex] == "i":
					self.commandPairs[device][commandIndex]["value"] = int(value)
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
			commandValue = str(command['value'])
			if (statusValue != commandValue) or (commandIndex == 0):
				# Create the json command to send
				commands = { 'commands' : command}
				try:
					finfo = gf(cf())
					status = self.cloud.sendcommand(self.ids[device],commands)
					success[commandIndex] = status['success']
					if status.get('msg','device is online') == 'device is offline':
						reason += self.names[device] + "is offLine"
					if not(success[commandIndex]):
						reason += self.names[device]+ "/" + commandCode + " cmnd  fail msg: " + status.get('msg','no msg')
						success[commandIndex] = False
						print("send command fail",reason)
				except Exception as err:	
					exc = f" File: {finfo.filename} Ln: {finfo.lineno} Type: {str(type(err))[8:-2]} Error: {str(err)}"
					print(exc)
					reason += exc
					success[commandIndex] = False

		time_sleep(1)

		try:
			finfo = gf(cf())
			status = self.cloud.getstatus(self.ids[device])
			stSuccess = status['success']
		except Exception as err:
			exc = f" File: {finfo.filename} Ln: {finfo.lineno} Type: {str(type(err))[8:-2]} Error: {str(err)}"
			print(exc)
			reason += exc
			stSuccess = False
		if stSuccess:
			statusValues = {}
			for item in status['result']:
				statusValues[item["code"]] = item["value"]
				if item["code"][:6] == "switch":
					 self.switchOn[device] = item["value"]
			self.devicesStatus[device] = statusValues
		else:
			reason += " Get Status Fail (result) " + self.names[device] + " "
			print("get status fail",reason)
		try:
			finfo = gf(cf())
			if status.get('msg','device is online') == 'device is offline':
				reason += self.names[device] + " is offLine"
				print(f"\n\n {self.names[device]} is offline")
				stSuccess = False
		except Exception as err:
			exc = f" File: {finfo.filename} Ln: {finfo.lineno} Type: {str(type(err))[8:-2]} Error: {str(err)}"
			print(exc)
			reason += exc

		return success,stSuccess,reason

	def getStatus(self):
		stSuccess = [False]*self.numberDevices
		status = []
		finfo = gf(cf())
		failReason= [""]
		for number in range(self.numberDevices):
			failReason.append("")
		for device in range(0,self.numberDevices):
			try:
				finfo = gf(cf())
				status = self.cloud.getstatus(self.ids[device])
				stSuccess[device] = status.get('success',False)
			except Exception as err:
				exc =  f" File: {finfo.filename} Ln: {finfo.lineno} Type: {str(type(err))[8:-2]} Error: {str(err)}"
				print(exc)
				failReason[device] += exc
			if stSuccess[device]:
				statusValues = {}
				for item in status['result']:
					debugPrint(self.debug,f"""Tuyacloud Get Status Results, item["code"]  {item["code"]} item["value"]  {item["value"]}""")
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
					print("184 try device = :",device)
					print("self.names[device] ",self.names[device])
					failReason[device] += " Get Status Fail (result) " + self.names[device] + " "
				except Exception as err:
					exc = f" File: {finfo.filename} Ln: {finfo.lineno} Type: {str(type(err))[8:-2]} Error: {str(err)}"
					print(exc)
					failReason[device] += exc
			# problem here was list object "spatus". "has no get
			try:
				finfo = gf(cf())
				if status.get('msg','device is online') == 'device is offline':
					failReason[device] += self.names[device] + " is offLine"
					stSuccess[device] = False
			except Exception as err:
				exc = f" File: {finfo.filename} Ln: {finfo.lineno} Type: {str(type(err))[8:-2]} Error: {str(err)}"
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
	config = class_config("config.cfg")
	config.scan_count = 0

	#import json
	
	# Opening JSON file
	with open('/home/pi/.tuyaJson/tinytuya.json', 'r') as jsonFile:
	#with open('/home/pi/modules/tinytuya.json', 'r') as jsonFile:
		# Reading from json file
		tinyTuyaJson = json.load(jsonFile)
	cloud = class_tuyaCloud(config,tinyTuyaJson)
	if cloud.numDevices > 0:
		for ind in range(cloud.numDevices):
			print("\n Device :  ",ind)
			print("\n",json.dumps(cloud.devices[ind],indent = 4),"\n")
			print("Proterties for :",ind)
			print("\n",json.dumps(cloud.properties[ind],indent = 4),"\n")

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
