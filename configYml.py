import yaml
import json
from paths import class_paths
import os
from sys import exit as sys_exit
from utility import prd as debugPrint

class class_configYml:
	def __init__(self,appName,functionName):
		paths = class_paths(appName)
		self.fileName = os.path.join(paths.config,functionName + ".yml")

		with open(self.fileName, "r") as file:
			self.data = yaml.safe_load(file)
   
		self.debug = self.data.get("Debug",False)
		debugPrint(self.debug,f"Yaml Config File used is {self.fileName}")
  
		self.appName = appName
		self.functionName = functionName
		self.progPath = paths.apps
		self.modulesPath = paths.modules
		self.configPath = paths.config
	
	def _printKeys(self, dictionary, prefix=''):
		for key, value in dictionary.items():
			if prefix:
				current_key = f'{prefix}["{key}"]'
			else:
				current_key = f'["{key}"]'
			debugPrint(self.debug,current_key)
			if isinstance(value, dict):
				self._printKeys(value, current_key)
				
	def printKeys(self):
		self._printKeys(self.data)

	def get(self, key):
		return self.data.get(key)

if __name__ == '__main__':
# Get base Configuration from paths.yml
	appName = "heat"
	functionName = "boiler"
	config = class_configYml(appName,functionName)
	#debugPrint(config.debug,,json.dumps(config.data,indent = 4))
	debugPrint(config.debug,f"yaml.dump(config.data, default_flow_style=False)\n {yaml.dump(config.data, default_flow_style=False)}")
	debugPrint(config.debug,f'config.data["Log"]["logBufferFlag"]  {config.data["Log"]["logBufferFlag"]} \n\n')		 
	debugPrint(config.debug,config.data["Tuya"]["spare2"]["valuesTypes"])
	choice = config.data["Schedules"]["choose"]
	debugPrint(config.debug,f"choice is {choice}")
	debugPrint(config.debug,f'Choice schedule is {config.data["Schedules"][choice]}')
	for index in range(len(config.data["Schedules"][choice])):
		debugPrint(config.debug,f'Day {index} schedule is {config.data["Schedules"][choice][index]}')
	
