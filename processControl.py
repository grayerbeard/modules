
# In this script, a paho.mqtt.client.Client is created and connected to thetarts topic.

#You can then subscribe to these topics in your userinterface.py Flask app to display 
#the status and restart count to the user.
#In this script, a paho.mqtt.client.Client is created and connected to the MQTT broker. 
#When a script fails, a message is published to the watchdog/status topic indicating 
#which script failed. The number of restarts is also tracked, and each time a script 
#fails, the count is published to the watchdog/restarts topic.

#You can then subscribe to these topics in your userinterface.py Flask app to display 
#the status and restart count to the user.

#Note that this is just a basic example. You'd likely want to add some error handling 
#for the MQTT operations, and possibly include more information in the MQTT messages 
#(such as the time of the failure, the error message, etc.). Also, don't forget to
#replace "localhost" with the address of your MQTT broker if it's not running on 
#the same machine.
#





import subprocess
import time
import paho.mqtt.client as mqtt

# Set up MQTT client
client = mqtt.Client("watchdog")
client.connect("localhost")  # Connect to the broker

def run_script(script_path, script_name):
    try:
        subprocess.check_call(["python3", script_path])
    except subprocess.CalledProcessError:
        # Publish a message to the MQTT broker
        client.publish("watchdog/status", f"{script_name} failed")
        return False
    return True

restart_count = 0
while True:
    if not run_script("/path/to/boiler.py", "boiler.py"):
        restart_count += 1
        client.publish("watchdog/restarts", str(restart_count))
        print("boiler.py failed, running boilerset.py")
        if not run_script("/path/to/boilerset.py", "boilerset.py"):
            print("boilerset.py failed, running shutdown_script.py")
            run_script("/path/to/shutdown_script.py", "shutdown_script.py")
            break
    time.sleep(10)  # Wait a bit before checking again

