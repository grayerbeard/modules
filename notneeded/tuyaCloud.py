# Standard library imports
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
			print("Exit at line 49")
			sys_exit()

		self.commandPairs = [[]]*config.numberCommandSets

		# old/current method
		self.codes = []
		self.codes.append(config.codes0)
		if not(config.codes1.__eq__("x")):
			self.codes.append(config.codes1)

		self.values = []
		self.values.append(config.values0)
		if not(config.values1.__eq__("x")):
			self.values.append(config.values1)

		self.valuesTypes = []
		self.valuesTypes.append(config.values0Types)
		if not(config.values1Types.__eq__("x")):
			self.valuesTypes.append(config.values1Types)

		#new method
		#self.codes = config.codes
		#self.values = config.values
		#self.valuesTypes = config.valuesTypes

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
					#self.commandPairs[device][ind] = dict(code = self.codes[device][ind],value = True)
					self.commandPairs[device].append(dict(code = self.codes[device][ind],value = True))
				elif str(self.values[device][ind]) == 'False':
					debugPrint(debug,"self.commandPairs[device] ",self.commandPairs[device])
					debugPrint(debug,"self.codes[device] ",self.codes[device])
					debugPrint(debug,"self.codes[device][ind] ",self.codes[device][ind])
					self.commandPairs[device].append(dict(code = self.codes[device][ind],value = False))
					#self.commandPairs[device][dict(code = self.codes[device][ind],value = False)]
					debugPrint(debug,"###self.commandPairs[device] ",self.commandPairs[device])
				elif self.valuesTypes[device][ind] == "s":
					#self.commandPairs[device][ind] = dict(code = self.codes[device][ind],value = str(self.values[device][ind]))
					self.commandPairs[device].append(dict(code = self.codes[device][ind],value = str(self.values[device][ind])))
					#self.commandPairs[device][dict(code = self.codes[device][ind],value = str(self.values[device][ind]))]
				elif self.valuesTypes[device][ind] == "i":
					#self.commandPairs[device][ind] = dict(code = self.codes[device][ind],value = int(self.values[device][ind]))
					self.commandPairs[device].append(dict(code = self.codes[device][ind],value = int(self.values[device][ind])))
					#self.commandPairs[device][dict(code = self.codes[device][ind],value = int(self.values[device][ind]))]
				else:
					debugPrint(debug,"THE Missing or incorrect code type", self.valuesTypes[device],self.codes[device]) ,
					sys_exit()

		for device in range(len(numcommandPairs)):
			for ind  in range(numcommandPairs[device]):
				debugPrint(debug,f"Command Pairs for device {device} are {self.commandPairs[device][ind]}")	


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
		#print("amended command Pairs: Target: ", device,code,value," \n",json.dumps(self.commandPairs[device],indent = 4),"\n")
		return result

	def upDateDevice(self,device):    # sets device to match values in commands

		# Assume online until get bad result and offline confirmed
		reason = ".."
		numberCommands =  len(self.commandPairs[device])
		success = [True]*self.numberDevices  
		#print(json.dumps(self.commandPairs[device]))
		for commandIndex in range(0,numberCommands):
			commandCode = self.commandPairs[device][commandIndex]["code"]
			statusValue = str(self.devicesStatus[device][commandCode])
			command = self.commandPairs[device][commandIndex]
			commandValue = str(command['value'])
			#print(commandCode,"  status : ",statusValue," command : ",commandValue)
			if (statusValue != commandValue) or (commandIndex == 0):
				#print("send cmnd",device,commandCode,commandValue)
				commands = { 'commands' : command}
				#print("Command : ",commandIndex,"\n",json.dumps(commands))
				try:
					#####################################################
					#finfo = gf(cf())
					#status = self.cloud.sendcommand(self.ids[device],commands)
					#print("Status after Command Send : ","\n",json.dumps(status))
					success[commandIndex] = status['success']
					if status.get('msg','device is online') == 'device is offline':
						reason += self.names[device] + "is offLine"
					if not(success[commandIndex]):
						reason += self.names[device]+ "/" + commandCode + " cmnd  fail msg: " + status.get('msg','no msg')
						print("send command fail",reason)
				except Exception as err:	
					exc = (finfo.filename,str(finfo.lineno),str(type(err))[8:-2],str(err)," Device: " + str(device))
					excRep.append(exc)
					print(exc)
					reason[device] += str(exc)

		time_sleep(1)

		try:
			finfo = gf(cf())
			status = self.cloud.getstatus(self.ids[device])
			stSuccess = status['success']
		except Exception as err:
			exc = (finfo.filename,str(finfo.lineno),str(type(err))[8:-2],str(err)," Device: " + str(device))
			excRep.append(exc)
			print(exc)
			reason[device] += str(exc)
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
				stSuccess = False
		except Exception as err:
			exc = (finfo.filename,str(finfo.lineno),str(type(err))[8:-2],str(err)," Device: " + str(device))
			excRep.append(exc)
			print(exc)
			reason[device] += str(exc)
		#except:	
		#	reason += "Get Status Fail (exception) " + self.names[device] + " "
		#	stSuccess = False

				

		#print ("devicesStatus : ",json.dumps(self.devicesStatus,indent = 4))
		return success,stSuccess,reason

	def getStatus(self):
		stSuccess = [False]*self.numberDevices
		status = []
		excRep = []
		finfo = gf(cf())
		for device in range(0,self.numberDevices):
			#try:
			if True:
				reason = [""]*self.numberDevices
				try:
					finfo = gf(cf())
					status = self.cloud.getstatus(self.ids[device])
					stSuccess[device] = status.get('success',False)
				except Exception as err:
					exc = (finfo.filename,str(finfo.lineno),str(type(err))[8:-2],str(err)," Device: " + str(device))
					excRep.append(exc)
					print(exc)
					reason[device] += str(exc)
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
											print("exception line 251 in tuyaCloud")		else:
								print("error TuyaCloud 182  ",item["code"],item["value"])
								sys_exit()
						else:
							statusValues[item["code"]] = item["value"]
					self.devicesStatus[device] = statusValues
				else:
					try:
						finfo = gf(cf())
						print("184 try device = :",device)
						print("self.names[device] ",self.names[device])
						reason[device] += " Get Status Fail (result) " + self.names[device] + " "
					except Exception as err:
						exc = (finfo.filename,str(finfo.lineno),str(type(err))[8:-2],str(err)," Device: " + str(device))
						excRep.append(exc)
						print(exc)
						reason[device] += str(exc)
				# problem here was list object "spatus". "has no get
				try:
					finfo = gf(cf())
					if status.get('msg','device is online') == 'device is offline':
						reason[device] += self.names[device] + " is offLine"
						stSuccess[device] = False
				except Exception as err:
					exc = (finfo.filename,str(finfo.lineno),str(type(err))[8:-2],str(err)," Device: " + str(device))
					excRep.append(exc)
					print(exc)
					reason[device] += str(exc)
					print("exception line 251 in tuyaCloud")
			#except:	
			#	reason += "Get Status Fail (exception) " + self.names[device] + " "
			#	stSuccess = False
		#print ("devicesStatus : \n",json.dumps(self.devicesStatus,indent = 4))
		return stSuccess,reason,self.devicesStatus,excRep


	def listDevices(self):
		# Display list of devicesapiKey
		devices = self.cloud.getdevices()
		return devices

	def deviceProperties(self,id):
		# Display Properties of Device
		properties = self.cloud.getproperties(id)
		print("Properties of Device:\n", properties)
		print("\n""\n")
		return properties

# not used
#	def deviceStatus(self,id):
#		# Display Status of DeviceStauts
#		status = self.cloud.getstatus(id)
#		#print("Status of Device:\n", status)
#		#print("\n""\n")
#		return status

#not used
#	def getTH(self,id):
#		status = self.cloud.getstatus(id)
#		#print(json.dumps(status))
#		temp = float(status['result'][0]['value'])/10
#		humidity = float(status['result'][1]['value'])
#		battery = status['result'][2]['value']
#		#print("Temperaturs : ", temp, " Humidity : ",humidity, "  Battery : ",battery)
#		return temp,humidity,battery

# not used
#	def getHP(self,id):
#		status = self.cloud.getstatus(id)
#		if status["success"] == True:
#			values = []
#			codes = []
#			for ind in range(len(status['result'])):
#				values.append(status['result'][ind]['value'])
#				codes.append(status['result'][ind]['code'])
#			#print("RValues : ",values,"  Codes : ",codes)
#			switch = status['result'][0]['value']
#			temp_set = int(status['result'][1]['value'])
#			temp_current = int(status['result'][2]['value'])
#			mode = status['result'][3]['value']
#			windspeed = int(status['result'][4]['value'])
#			c_f	= status['result'][5]['value']
#			#print("Switch : ", switch,"temp_set : ", temp_set, " temp_current : ",temp_current, "  mode : ",mode, "  windspeed : ",windspeed, "  c_f : ",c_f)
#		else:
#			#print("Get Status Fail with message : ",status.get("msg","No message"))
#			switch,temp_set,temp_current,mode,windspeed,c_f = "","","","","",""
#		return switch,temp_set,temp_current,mode,windspeed,c_f

# not used
#	def operateSwitch(self,switchNumber,stateWanted):    # Send Command - Turn on switch
#
#		# Assume online until get bad result and offline confirmed
#		printMessage =  ""
#		reason = ""
#		opFail = False
#
#		commands = {
#			'commands': 	[
#								{
#								'code': self.codes[switchNumber],
#								'value': stateWanted
#								}, 
#								{
#								'code': 'countdown_1',
#								'value': 0
#								}
#							]
#					}
#		successfullResult = False
#		try:
#			status = self.cloud.sendcommand(self.ids[switchNumber],commands)
#			#print(status, "  :  ",status.get('msg','device is online'))
#			success = status['success']
#			if status.get('msg','device is online') == 'device is offline':
#				opFail = True
#				reason += names[switchNumber] + " is offLine"
#		except:	
#			printMessage += "Cloud Send Command Fail"
#			reason += "Cloud Send Command Fail"
#			opFail = True
#
#		if successfullResult:
#			switchOn = stateWanted
#			self.lastSwitchOn[switchNumber] = switchOn
#			if stateWanted:
#				printMessage += " Switch on OK " + self.names[switchNumber]
#			else:
#				printMessage += " Switch off OK "+ self.names[switchNumber]
#		else:
#			# not successful so return last known state and error flag
#			switchOn = self.lastSwitchOn[switchNumber]
#		print(status)
#		return switchOn,opFail,printMessage,reason

# test routine rin when script run direct
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


	# uncomment line below to get list of devices
	#cloud.listDevices()
	
	# uncomment three lines below and set id to check a particular device 
	#cloud.deviceProperties(ids[1])
	#cloud.deviceStatus(id)

	# uncomment three lines below and set id to check a particular device 
	#id = 'bf6f1291cc4b30aa8d1wsv'
	#properties = cloud.deviceProperties(id)

	#switchOn,opFail,printMessage,reason = cloud.operateSwitch(1,False)
	 
	#properties = cloud.deviceProperties(id)
	
	#print("\n \n ")
	#print(status)
	#print("\n \n")
	
	#print(online)


	count = 0

	while count < 5  :
		#status = cloud.deviceStatus(id)
	# print("Properties:"	, propertiecommandPairss)
	# print("Status:",status)
		temp, humidity, battery = cloud.getTH(id)
		print(temp,humidity,battery)
		print(datetime.now())
		count += 1
		#time_sleep(10 * 60)
		print(count)

	# uncomment three lines below and set id to check a particular device 
	#id = "01303121a4e57cb7ca0c"  
	#cloud.deviceProperties(id)
	#cloud.deviceStatus(id)	


	# test power switch that has a switch code of "switch_1"
	# Using id found from print out doing above
	# note we use switchNumber 0

	print("Test power switch")

	switchNumber = 0
	id = "bf5723e4b65de4a64fteqz"
	code = "switch_1"

	stateWanted = False
	switchOn, successfullResult, offLine = cloud.operateSwitch(switchNumber,id,code,stateWanted)
	if successfullResult:
		print("worked ok")
		if switchOn:
			print("Switch On")
		else:
			print("Switch off")
	else:
		print("Switch Operation failed")
		if offLine:
			print("Device is Offline")
	time_sleep(5)

	stateWanted = True
	switchOn, successfullResult, offLine = cloud.operateSwitch(switchNumber,id,code,stateWanted)
	if successfullResult:
		print("worked ok")
		if switchOn:
			print("Switch On")
		else:
			print("Switch off")
	else:
		print("Switch Operation failed")
		if offLine:
			print("Device is Offline")
	time_sleep(5)

	stateWanted = False
	switchOn, successfullResult, offLine = cloud.operateSwitch(switchNumber,id,code,stateWanted)
	if successfullResult:
		print("worked ok")
		if switchOn:
			print("Switch On")
		else:
			print("Switch off")
	else:
		print("Switch Operation failed")	
		if offLine:
			print("Device is Offline")

	# test power on off of heat pump that has power switch code of "switch"
	# Using id found from print out doing above
	# note we use switchNumber 1

	print("Test power switch on/off of Heat Pump")

	switchNumber = 1
	id = "01303121a4e57cb7ca0c"
	code = "switch"
	stateWanted = False

	switchOn, successfullResult, offLine = cloud.operateSwitch(switchNumber,id,code,stateWanted)
	if successfullResult:
		print("worked ok")
		if switchOn:
			print("Switch On")
		else:
			print("Switch off")
	else:
		print("Switch Operation failed")
		if offLine:
			print("Device is Offline")

	time_sleep(5)

	stateWanted = True
	switchOn, successfullResult, offLine = cloud.operateSwitch(switchNumber,id,code,stateWanted)
	if successfullResult:
		print("worked ok")
		if switchOn:
			print("Switch On")
		else:
			print("Switch off")
	else:
		print("Switch Operation failed")

		if offLine:
			print("Device is Offline")

	time_sleep(20)

	stateWanted = False
	switchOn, successfullResult, offLine = cloud.operateSwitch(switchNumber,id,code,stateWanted)
	if successfullResult:
		print("worked ok")
		if switchOn:
			print("Switch On")
		else:
			print("Switch off")
	else:
		print("Switch Operation failed")	
		if offLine:
			print("Device is Offline")
