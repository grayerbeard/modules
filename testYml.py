import yaml
import paths
import os
import json

from paths import class_paths

def loadYmlFile(filename):
    with open(filename, 'r') as file:
        return yaml.safe_load(file)

def saveYmlFile(filename, data):
    with open(filename, 'w') as file:
        yaml.safe_dump(data, file)
        
def saveTextFile(filename, data):
    with open(filename, 'w') as file:
       file.write(data)

def main():
    appName = "heat"
    paths = class_paths(appName)
    if paths.pathsOK:
        print("PathsOK")
    else:
        print("Paths NOT OK")
    print(paths.message)
    
    filename = input("Please enter the name of your YAML file: ")
    fullFilename = os.path.join(paths.config,filename)
    data = loadYmlFile(fullFilename)

    testFilename = 'test-' + filename
    fullTestFilename = os.path.join(paths.config,testFilename)
    saveYmlFile(fullTestFilename, data)

    print(f"File has been saved as {testFilename}.")
    
    testData = loadYmlFile(fullTestFilename)
    
    # Create Output File
    fileText =  f"Original Data:\n {json.dumps(data,indent=4)} \n\nTest Data:\n {json.dumps(testData,indent=4)}"
    
    saveTextFile("dump.txt", fileText)

if __name__ == "__main__":
    main()
