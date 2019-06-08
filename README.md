# Objectives
* To measure the IAQ (Indoor Air Quality) Index & Accuracy, Air Pressure (mbar), Humidity (%RH), Temperature (°C), Illuminance (Lux).
* To display values in an Air Quality Station and in Domoticz.
* To notify if the Air Quality is below threshold.

## Solution
An "Air Quality Station" using [Tinkerforge](https://www.tinkerforge.com/en) Building Blocks Master Brick & WiFi Extension and Bricklets Air Quality, LCD 20x4 display, RGB LED, Ambient Light.
The LCD 20x4 display to show the
* IAQ Index (0-50=good, 51-100=average, 101-150=little bad, 151-200=bad, 201-300=worse, 301-500=very bad)
* IAQ Index Accuracy (Unreliable, Low, Medium, High)
* Air Quality (good to very bad)
* Temperature (C). Humidity (%), Air Pressure (mb), Illuminance (lx)
The RGB LED indicates the Air Quality good (green), average (yellow), (little) bad (red), worse & very bad (red)</li>

Domoticz Plugin "Air Quality Monitor" polls in regular interval data from the "Air Quality Station".
This plugin has following devices (Type,SubType):
* IAQ Index (Air Quality,Voltcraft CO-20), IAQ Index Accuracy (General,Alert), Air Quality (General, Alert, [good, average, (little) bad, worse,bad]
* Temperature (Temp,LaCrosse TX3), Humidity (Humidity,LaCrosse TX3), Air Pressure (General,Barometer), Ambient Light (Lux,Lux)
* LCD Backlight (Light/Switch,Switch), Status (General,Text)

## Hardware
* Raspberry Pi 3B+ (Domoticz Server)
__Tinkerforge__
* Master Brick 2.1 [ref](https://www.tinkerforge.com/en/doc/Hardware/Bricks/Master_Brick.html#master-brick)
* WiFi Master Extension 2.0 [ref](https://www.tinkerforge.com/en/doc/Hardware/Master_Extensions/WIFI_V2_Extension.html)
* Air Quality Bricklet [ref](https://www.tinkerforge.com/en/doc/Hardware/Bricklets/Air_Quality.html)
* LCD 20x4 Bricklet 1.2 [ref](https://www.tinkerforge.com/en/doc/Hardware/Bricklets/LCD_20x4.html)
* RGB LED Bricklet 2.0 [ref](https://www.tinkerforge.com/en/doc/Hardware/Bricklets/RGB_LED_V2.html)
* Ambient Light Bricklet 2.0 (old) [ref](https://www.tinkerforge.com/en/doc/Hardware/Bricklets/Ambient_Light_V3.html#ambient-light-v3-bricklet) [V2.0 not sold anymore]
* Weather Station Case (transparent) [ref](https://www.tinkerforge.com/en/shop/cases/weather-station-case-transparent.html)

## Software
Versions for developing & using this plugin.
* Raspberry Pi Raspian 4.14
* Domoticz Home Automation System V4.1
* Tinkerforge Python Binding v2.1.22
* Python 3.5.3
* Thonny 3.1.2 (Python IDE)

## Prepare Tinkerforge Python API bindings
The Tinkerforge Python API bindings are required, installed using pip3.
Pip3 installs the bindings in a common dist-packages folder, which is on the Raspberry Pi Domoticz Server, folder:
/usr/lib/python3/dist-packages

Running pip3:
``` 
sudo pip3 install tinkerforge
``` 
Log Output:
Collecting tinkerforge
Installing collected packages: tinkerforge
Successfully installed tinkerforge-2.1.22

The Tinkerforge Python API bindings are installed in folder:
/usr/local/lib/python3.5/dist-packages

Check the content results in two folders, from which the folder tinkerforge is required
``` 
ls /usr/local/lib/python3.5/dist-packages
tinkerforge tinkerforge-2.1.22.dist-info
``` 

## Plugin Folder and File
Each plugin requires a dedicated folder which contains the plugin, mandatory named plugin.py.
mkdir /home/pi/domoticz/plugins/airqualitymonitor

As a starter, take the template from [here](https://github.com/domoticz/domoticz/blob/master/plugins/examples/BaseTemplate.py).
Save as plugin.py in the folder /home/pi/domoticz/plugins/airqualitymonitor

## Python Plugin Path to Tinkerforge API Bindings
In the Python Plugin code amend the import path to enable using the Tinkerforge API Bindings:
``` 	
	from os import path
	import sys
	sys.path
	sys.path.append('/usr/local/lib/python3.5/dist-packages')
``` 

## Development Setup
Development PC:
* Thonny to develop the Python Plugin
* A shared drive Z: is defined pointing to /home/pi/domoticz
* Browser Tab Domoticz Web UI > Setup > Log
* Browser Tab Domoticz Web UI > Setup > Hardware
* Browser Tab Domoticz Web UI > Setup > Devices
* WinSCP session connected to the Domoticz server
* Putty session connected to the Domoticz server

The Browser tabs required to add the new hardware with its device and monitor if the plugin code is running without errors.

## Development Iteration
The development process step used are:
1. Thonny develop z:\plugins\airqualitymonitor\plugin.py
2. Make changes and save plugin.py
3. Restart Domoticz from Terminal: sudo service domoticz.sh restart
4. Wait a moment and refresh the Browser Tab Domoticz Web UI > Log
5. Check the log and fix as required

!IMPORTANT!
In the Domoticz Web UI > Setup > Settings,  enable accepting new hardware.
This is required to add the new hardware with its device and monitor if the plugin code is running without errors.

## Tinkerforge Master Brick and Bricklets
Ensure the Master Brick and Bricklets are running with the latest firmware.
To update the Tinkerforge [Brick Viewer](https://www.tinkerforge.com/en/doc/Software/Brickv.html#brickv) is required.
For Tinkerforge development purposes installed the Brick Viewer and the required Brick Daemon on a Linux PC (called the piDevBook as running [Raspberry Pi Desktop](https://www.raspberrypi.org/downloads/raspberry-pi-desktop/).
Steps to update the Master Brick and Bricklets:
1. Connect the Master Brick to the piDevBook using USB mini cable
2. Start Brick  Viewer (ensure latest version, used v2.4.4)
3. Connect localhost:4223
4. Check if Master brickand Bricklets found
5. Select Update and check version differences
6. Update Master Brick
a. Button Erase - press and hold (DO NOT RELEASE)!
b. Button Reset - press and release
c. Button Erase - release!
The Master Brick Blue LED is turned off indicating boot mode.
7. The Brick Viewer shows only the Brick Tab
8. Refresh serial port= Serial Port: /dev/ttyACMo, Fiirmware: Master (2.4.10)
9. Flash
10. Master Brick reboots > Blue LED turns on and the Brick Viewer shows tabs Brick and Bricklets

See next Air Quality Prototype

## Air Quality Monitor Prototype
Build the prototype by connecting the Tinkerforge building blocks (see hardware).
Connect the Master Brick to a device running the Brick Deamon and Viewer.
Just in a nutshell the actions taken to setup the Tinkerforge building blocks using the Tinkerforge Brick Viewer.
* Update the devices firmware
* Set the WiFi master extension fixed IP address in client mode
* Obtain the UID's of the Tinkerforge bricklets as required by the Python plugin

After setting up the Tinkerforge building blocks, reset the master brick and check if the master brick can be reached via WLAN:
``` 
ping tf-wifi-ext-ip-address
``` 

## Domoticz Web UI's
Open windows Domoticz Setup > Hardware, Domoticz Setup > Log, Domoticz Setup > Devices
This is required to add the new hardware with its device and monitor if the plugin code is running without errors.

## Create folder
```
cd /home/pi/domoticz/plugins/airqualitymonitor
```

## Create the plugin
The plugin has a mandatory filename **plugin.py** located in the plugin folder /home/pi/domoticz/plugins/airqualitymonitor.
For Python development Thonny, running on a Windows 10 device, is used.

Lookup for details in the source code **plugin.py** (well documented).

**Pseudo Code**
* INIT: set self vars to handle heartbeat count,ip connection state and UID list
* FIRST TIME: _onStart_ to create the Domoticz Devices and configure Tinkerforge Building Blocks
* NEXT TIME(S):
	*_onCommand_ to handle state changes
		* LCD Backlight on or off
	*_onHearbeat_ to update LCD display and Domoticz devices

The devices are manually added to the Domoticz Dashboard.
In addition a room "Air Quality Monitor" is defined with all the AQM devices and a simple floorplan.

## Restart Domoticz
Restart Domoticz to find the plugin:
sudo systemctl restart domoticz.service

**Note**
When making changes to the Python plugin code, ensure to restart Domoticz and refresh any of the Domoticz Web UI's.
This is the iteration process during development - build the solution step-by-step.

## Domoticz Add Hardware Air Quality Monitor
**IMPORTANT**
Prior adding, set in the Domoticz Settings the option to allow new hardware.
If this option is not enabled, no new Air Quality device is created.
Check in the Domoticz log as error message Python script at the line where the new device is used
(i.e. Domoticz.Debug("Device created: "+Devices[1].Name))

In Domoticz Web UI, select tab Setup > Hardware and add the new hardware Air Quality Monitor.
The initial check interval is set at 60 seconds. This is a good value for testing, but for final version set to higher value like every 5 minutes (300 seconds).

## Add Hardware - Check the Domoticz Log
After adding,ensure to check the Domoticz Log (Domoticz Web UI, select tab Setup > Log)
Example:
```
2019-06-08 19:14:25.934 Status: (AQM) Started. 
2019-06-08 19:14:26.551 (AQM) Air Quality Monitor starting 
2019-06-08 19:14:26.551 (AQM) Debug logging mask set to: PYTHON PLUGIN QUEUE IMAGE DEVICE CONNECTION MESSAGE ALL 
2019-06-08 19:14:26.551 (AQM) 'Address':'192.168.1.114' 
2019-06-08 19:14:26.551 (AQM) 'HardwareID':'8' 
2019-06-08 19:14:26.551 (AQM) 'Mode6':'Debug' 
2019-06-08 19:14:26.551 (AQM) 'Version':'1.0.0 (Build 20190608)' 
2019-06-08 19:14:26.551 (AQM) 'Database':'/home/pi/domoticz/domoticz.db' 
2019-06-08 19:14:26.551 (AQM) 'DomoticzHash':'b06fb6b60' 
2019-06-08 19:14:26.551 (AQM) 'DomoticzVersion':'4.10881' 
2019-06-08 19:14:26.551 (AQM) 'Mode2':'40' 
2019-06-08 19:14:26.551 (AQM) 'Mode5':'60' 
2019-06-08 19:14:26.551 (AQM) 'StartupFolder':'/home/pi/domoticz/' 
2019-06-08 19:14:26.551 (AQM) 'HomeFolder':'/home/pi/domoticz/plugins/airqualitymonitor/' 
2019-06-08 19:14:26.552 (AQM) 'Language':'en' 
2019-06-08 19:14:26.552 (AQM) 'Mode1':'6yLduG,Jvj,BHN,Jng,yyc' 
2019-06-08 19:14:26.552 (AQM) 'Author':'rwbL' 
2019-06-08 19:14:26.552 (AQM) 'Port':'4223' 
2019-06-08 19:14:26.552 (AQM) 'Name':'AQM' 
2019-06-08 19:14:26.552 (AQM) 'UserDataFolder':'/home/pi/domoticz/' 
2019-06-08 19:14:26.552 (AQM) 'Key':'AirQualityMonitor' 
2019-06-08 19:14:26.552 (AQM) 'DomoticzBuildTime':'2019-06-08 15:28:08' 
2019-06-08 19:14:26.552 (AQM) Device count: 0 
2019-06-08 19:14:26.552 (AQM) Creating new devices ... 
2019-06-08 19:14:26.552 (AQM) Creating device 'IAQ Index'. 
2019-06-08 19:14:26.553 (AQM) Device created: AQM - IAQ Index 
2019-06-08 19:14:26.553 (AQM) Creating device 'IAQ Index Accuracy'. 
2019-06-08 19:14:26.554 (AQM) Device created: AQM - IAQ Index Accuracy 
2019-06-08 19:14:26.554 (AQM) Creating device 'Air Quality'. 
2019-06-08 19:14:26.555 (AQM) Device created: AQM - Air Quality 
2019-06-08 19:14:26.556 (AQM) Creating device 'Temperature'. 
2019-06-08 19:14:26.556 (AQM) Device created: AQM - Temperature 
2019-06-08 19:14:26.557 (AQM) Creating device 'Humidity'. 
2019-06-08 19:14:26.557 (AQM) Device created: AQM - Humidity 
2019-06-08 19:14:26.558 (AQM) Creating device 'Air Pressure'. 
2019-06-08 19:14:26.558 (AQM) Device created: AQM - Air Pressure 
2019-06-08 19:14:26.559 (AQM) Creating device 'Ambient Light'. 
2019-06-08 19:14:26.560 (AQM) Device created: AQM - Ambient Light 
2019-06-08 19:14:26.560 (AQM) Creating device 'Backlight'. 
2019-06-08 19:14:26.561 (AQM) Device created: AQM - Backlight 
2019-06-08 19:14:26.561 (AQM) Creating device 'Status'. 
2019-06-08 19:14:26.562 (AQM) Device created: AQM - Status 
2019-06-08 19:14:26.562 (AQM) Creating new devices: OK 
2019-06-08 19:14:26.562 (AQM) UIDs:6yLduG,Jvj,BHN,Jng,yyc 
2019-06-08 19:14:26.562 (AQM) SetMasterStatusLed - UID:6yLduG 
2019-06-08 19:14:26.571 (AQM) Master Status LED disabled. 
2019-06-08 19:14:26.672 (AQM) SetLCDBacklight - UID:BHN 
2019-06-08 19:14:26.681 (AQM) LCD Backlight ON. 
2019-06-08 19:14:26.782 (AQM - Backlight) Updating device from 0:'' to have values 1:'0'. 
2019-06-08 19:14:26.788 (AQM) SetRGBLEDStatusLed - UID:Jng 
2019-06-08 19:14:26.799 (AQM) RGB LED Status LED disabled. 
2019-06-08 19:14:26.901 (AQM) ConfigAirQuality - UID:Jvj 
2019-06-08 19:14:26.912 (AQM) Air Quality Status LED disabled. 
2019-06-08 19:14:26.548 Status: (AQM) Entering work loop. 
2019-06-08 19:14:26.549 Status: (AQM) Initialized version 1.0.0 (Build 20190608), author 'rwbL' 
2019-06-08 19:14:26.856 Status: dzVents: Error (2.4.23): Discarding device. No last update info found: {["data"]={["levelVal"]=0, ["hardwareID"]=16, ["hardwareType"]="Air Quality Monitor", ["hardwareName"]="AQM", ["maxDimLevel"]=100, ["hardwareTypeValue"]=94, ["_state"]="On", ["protected"]=false, ["_nValue"]=1, ["usedByCamera"]=false, ["unit"]=8, ["icon"]="lightbulb"}, ["changed"]=true, ["id"]=44, ["rawData"]={"0"}, ["switchTypeValue"]=0, ["switchType"]="On/Off", ["lastLevel"]=255, ["batteryLevel"]=0, ["deviceType"]="Light/Switch", ["signalLevel"]=0, ["baseType"]="device", ["description"]="", ["name"]="AQM - Backlight", ["deviceID"]="", ["timedOut"]=false, ["subType"]="Switch", ["lastUpdate"]=""} 
2019-06-08 19:14:27.014 (AQM) Heartbeat set: 60 
2019-06-08 19:14:27.014 (AQM) Pushing 'PollIntervalDirective' on to queue 
2019-06-08 19:14:27.014 (AQM) Processing 'PollIntervalDirective' message 
2019-06-08 19:14:27.014 (AQM) Heartbeat interval set to: 60. 
2019-06-08 19:14:36.550 (AQM) Pushing 'onHeartbeatCallback' on to queue 
2019-06-08 19:14:36.581 (AQM) Processing 'onHeartbeatCallback' message 
2019-06-08 19:14:36.581 (AQM) Calling message handler 'onHeartbeat'. 
2019-06-08 19:14:36.581 (AQM) onHeartbeat called. Counter=60 (Heartbeat=60) 
2019-06-08 19:14:36.582 (AQM) IP Connected created 
2019-06-08 19:14:36.584 (AQM) Devices created - OK 
2019-06-08 19:14:36.596 (AQM) IP Connection - OK 
2019-06-08 19:14:36.602 (AQM - IAQ Index) Updating device from 0:'' to have values 125:'0'. 
2019-06-08 19:14:36.612 (AQM) AQM - IAQ Index-IAQ Index:125 
2019-06-08 19:14:36.612 (AQM - IAQ Index Accuracy) Updating device from 0:'No Alert!' to have values 4:'Unreliable'. 
2019-06-08 19:14:36.622 (AQM) AQM - IAQ Index Accuracy-IAQ IndexAccuracy:4,Unreliable 
2019-06-08 19:14:36.622 (AQM - Air Quality) Updating device from 0:'No Alert!' to have values 2:'LITTLE BAD'. 
2019-06-08 19:14:36.632 (AQM) Air Quality:2,LITTLE BAD 
2019-06-08 19:14:36.632 (AQM - Temperature) Updating device from 0:'' to have values 0:'21'. 
2019-06-08 19:14:36.640 (AQM) AQM - Temperature-Temperature:21 
2019-06-08 19:14:36.640 (AQM - Humidity) Updating device from 0:'' to have values 54:'1'. 
2019-06-08 19:14:36.649 (AQM) AQM - Humidity-Humidity:54 
2019-06-08 19:14:36.649 (AQM - Air Pressure) Updating device from 0:'1021.34;0' to have values 0:'1017;0'. 
2019-06-08 19:14:36.658 (AQM) AQM - Air Pressure-Air Pressure:1017 
2019-06-08 19:14:36.658 (AQM) Air Quality Devices updated 
2019-06-08 19:14:36.666 (AQM - Ambient Light) Updating device from 0:'' to have values 0:'150'. 
2019-06-08 19:14:36.675 (AQM) AQM - Ambient Light-Lux:150 
2019-06-08 19:14:36.675 (AQM) Tinkerforge updating... 
2019-06-08 19:14:36.675 (AQM) LCD Display cleared 
2019-06-08 19:14:36.679 (AQM) LCD Lines written 
2019-06-08 19:14:36.680 (AQM - Status) Updating device from 0:'' to have values 0:'OK: 125,21,54,1017'. 
2019-06-08 19:14:36.702 (AQM) OK: 125,21,54,1017 
2019-06-08 19:14:36.805 (AQM) Update - OK. 
```

## Domoticz Log Entry AQM Poll with Debug=True
The Air Quality Monitor runs every 60 seconds (Heartbeat interval) which is shown in the Domoticz log.
```
2019-06-08 19:16:43.118 (AQM) Pushing 'onHeartbeatCallback' on to queue 
2019-06-08 19:16:43.158 (AQM) Processing 'onHeartbeatCallback' message 
2019-06-08 19:16:43.158 (AQM) Calling message handler 'onHeartbeat'. 
2019-06-08 19:16:43.158 (AQM) onHeartbeat called. Counter=240 (Heartbeat=60) 
2019-06-08 19:16:43.159 (AQM) IP Connected created 
2019-06-08 19:16:43.162 (AQM) Devices created - OK 
2019-06-08 19:16:43.175 (AQM) IP Connection - OK 
2019-06-08 19:16:43.182 (AQM - IAQ Index) Updating device from 133:'0' to have values 121:'0'. 
2019-06-08 19:16:43.189 (AQM) AQM - IAQ Index-IAQ Index:121 
2019-06-08 19:16:43.189 (AQM - IAQ Index Accuracy) Updating device from 3:'Low' to have values 3:'Low'. 
2019-06-08 19:16:43.198 (AQM) AQM - IAQ Index Accuracy-IAQ IndexAccuracy:3,Low 
2019-06-08 19:16:43.198 (AQM - Air Quality) Updating device from 2:'LITTLE BAD' to have values 2:'LITTLE BAD'. 
2019-06-08 19:16:43.206 (AQM) Air Quality:2,LITTLE BAD 
2019-06-08 19:16:43.207 (AQM - Temperature) Updating device from 0:'21' to have values 0:'21'. 
2019-06-08 19:16:43.214 (AQM) AQM - Temperature-Temperature:21 
2019-06-08 19:16:43.214 (AQM - Humidity) Updating device from 54:'1' to have values 54:'1'. 
2019-06-08 19:16:43.222 (AQM) AQM - Humidity-Humidity:54 
2019-06-08 19:16:43.222 (AQM - Air Pressure) Updating device from 0:'1017;0' to have values 0:'1017;0'. 
2019-06-08 19:16:43.229 (AQM) AQM - Air Pressure-Air Pressure:1017 
2019-06-08 19:16:43.229 (AQM) Air Quality Devices updated 
2019-06-08 19:16:43.239 (AQM - Ambient Light) Updating device from 0:'138' to have values 0:'130'. 
2019-06-08 19:16:43.246 (AQM) AQM - Ambient Light-Lux:130 
2019-06-08 19:16:43.246 (AQM) Tinkerforge updating... 
2019-06-08 19:16:43.247 (AQM) LCD Display cleared 
2019-06-08 19:16:43.250 (AQM) LCD Lines written 
2019-06-08 19:16:43.251 (AQM - Status) Updating device from 0:'OK: 133,21,54,1017' to have values 0:'OK: 121,21,54,1017'. 
2019-06-08 19:16:43.261 (AQM) OK: 121,21,54,1017 
2019-06-08 19:16:43.364 (AQM) Update - OK. 
```

## ToDo
See TODO.md

## Version
v1.0.0 (Build 20190608)

