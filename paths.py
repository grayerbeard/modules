# This class module must be in the same folder as the main apps
# It loads in a ymal called paths.yml and then provides
# various folder locations.
# So for example if the folder used for the Git folders on 
# your windows laptop is at ~/OneDrive/Git
# on windows the apps folder is ~/OneDrive/Git/myApps
# the modules on windows are in ~/OneDrive/Git/modules
# and the config files are in ~/OneDrive/Git/config/heatConfig
# and on the Raspberry pi the equivalent folders are
# /home/pi/myApps
# /home/pi/modules
# /home/pi/config/config
# Then the file paths yml file would be
#   path_W_git: Git
#   path_W_myApps: myApps
#   path_W_modules: modules
#   path_W_config: config
#   path_L_myApps: myApps
#   path_L_modules: modules
#   path_L_config: .config   
#
# and the program below will figure out all the right locations
# The locations are then obtained using
# paths.apps
# paths.modules
# paths.config

import os
from sys import exit as sys_exit
import yaml

class class_paths:
    def __init__(self,appName):
        # Will lok for this file and exit if its missing
        pathsYmlFile = "paths.yml"
        try:
            with open(pathsYmlFile, 'r') as f:
                self.pathsConfig = yaml.safe_load(f)
        except FileNotFoundError:
            print(f"Error: file not found {pathsYmlFile}")
            sys_exit()
        if os.name == 'nt':
            self.home = os.path.join(self.get_onedrive_path(),self.pathsConfig["path_W_git"])
            relativePathApps = self.pathsConfig["path_W_myApps"]
            relativePathModules = self.pathsConfig["path_W_modules"]
            relativePathConfig = os.path.join(self.pathsConfig["path_W_config"],
                                              appName)
        else:
            # Assume now we on a Raspberry Pi
            # Home will be /home/pi if user is "pi" 
            self.home = os.path.expanduser("~")
            relativePathApps = self.pathsConfig["path_L_myApps"]
            relativePathModules = self.pathsConfig["path_L_modules"]
            relativePathConfig = os.path.join(self.pathsConfig["path_L_config"],
                                              appName)
        self.apps = os.path.join(self.home, relativePathApps)
        self.modules = os.path.join(self.home, relativePathModules)
        self.config = os.path.join(self.home, relativePathConfig)
        self.check_paths()

    def get_onedrive_path(self):
        import winreg
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as key:
            return winreg.QueryValueEx(key, "OneDrive")[0]

    def check_paths(self):
        self.pathsOK = True
        self.message = ""
        if os.path.isdir(self.apps):
           self. message += f"Apps directory exists: {self.apps}\n"
        else:
            self.pathsOK = False
            self.message += f"Apps directory does not exist: {self.apps}\n"
        if os.path.isdir(self.modules):
            self.message += f"Modules directory exists: {self.modules}\n" 
        else:
            self.pathsOK = False
            self.message += f"Modules directory does not exist: {self.modules}\n"
        if os.path.isdir(self.config):
            self.message += f"Config directory exists: {self.config}\n"
        else:
            self.pathsOK = False
            self.message += f"Config directory does not exist: {self.config}\n"

if __name__ == '__main__':
# Get base Configuration from paths.yml
    appName = "heat"
    paths = class_paths(appName)
    if paths.pathsOK:
        print("PathsOK")
    else:
        print("Paths NOT OK")
    print(paths.message)