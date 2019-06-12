# Indoor Air Quality Monitor 
v1.1.1 (Build 20190612)

# Objectives
* To measure the Indoor Air Quality Index, Condition and Accuracy, Air Pressure, Humidity, Temperature, Illuminance.
* To display values in an Indoor Air Quality Station and in Domoticz.
* To enable additional functionality by using scripts (preferred dzVents Lua scripts), i.e. switch LCD backlight, switch room light depending Lux threshold.

_Abbreviations_: IAQ=Indoor Air Quality, GUI=Domoticz Web UI.

## Solution
An **Indoor Air Quality Station** is build out of [Tinkerforge](https://www.tinkerforge.com/en) Building Blocks:
Master Brick with WiFi Extension, Bricklets Air Quality, LCD 20x4, RGB LED, Ambient Light.

![domoticz-tinkerforge-airqualitymonitor-p2](https://user-images.githubusercontent.com/47274144/59162141-56854400-8aec-11e9-843a-335f28a6f059.png)

The **Air Quality Bricklet** measures the IAQ Index (ppm), IAQ Condition, IAQ Accuracy, Air Pressure (mbar), Humidity (%), Temperature (C).
_Referencing Tinkerforge [documentation](https://www.tinkerforge.com/en/doc/Hardware/Bricklets/Air_Quality.html#air-quality-bricklet):_
``` 
The IAQ index is a measurement for the quality of air. To calculate the IAQ index the Bricklet detects ethane, isoprene (2-methylbuta-1,3-diene), ethanol, acetone and carbon monoxide (often called VOC, volatile organic components) by adsorption. These gas measurements are combined with the measurements of air pressure, humidity and temperature to calculate the final IAQ index.
``` 
* There are 6 IAQ Condition Levels with range=condition (color):
0-50=Good (green), 51-100=Moderate (yellow), 101-150=Unhealthy sensitive groups (orange), 151-200=Unhealthy (red), 201-300=Very Unhealthy (purple), 301-500=Hazardous (maroon).<br/>
* The IAQ Index Accuracy has 4 levels Unreliable, Low, Medium, High.

The **Ambient Light Bricklet** measures the Illuminance (lx).

The **LCD 20x4 Bricklet** displays the IAQ Index ppm, IAQ Condition, Temperature C, Humidity %, Air Pressure mbar, Illuminance lx.

The **RBG LED Bricklet** indicates the IAQ Condition Level Color.

The Domoticz Plugin **Indoor Air Quality Monitor** polls in regular intervals data from the **Indoor Air Quality Station**.
The **Domoticz Indoor Air Quality Devices** created are - Name (Type,SubType):
* Index (General,Custom Sensor), Index Accuracy (General,Alert), Air Quality (General, Alert [Text=Level].
* Temperature (Temp,LaCrosse TX3),Humidity (Humidity,LaCrosse TX3),Air Pressure (General,Barometer),Ambient Light (Lux,Lux).
* LCD Backlight (Light/Switch,Switch), Status (General,Text).
_Note:_
Enhanced functionality, like switch LCD backlight, switch lights (depending Lux) are build using dzVents Lua scripts.

![domoticz-plugin-iaqm-d2](https://user-images.githubusercontent.com/47274144/59341287-e6530a00-8d07-11e9-87e0-0689e8ad68f8.png)

![domoticz-tinkerforge-airqualitymonitor-f](https://user-images.githubusercontent.com/47274144/59162130-335a9480-8aec-11e9-8ae6-77c00884e2a1.png)

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
``` 
/usr/lib/python3/dist-packages
``` 
Running pip3:
``` 
sudo pip3 install tinkerforge
``` 
_Log Output_
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
``` 
mkdir /home/pi/domoticz/plugins/airqualitymonitor
``` 

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
* GUI > Setup > Log
* GUI > Setup > Hardware
* GUI > Setup > Devices
* WinSCP session connected to the Domoticz server
* Putty session connected to the Domoticz server

The various GUI's are required to add the new hardware with its devices and monitor if the plugin code is running without errors.

## Development Iteration
The development process step used are:
1. Thonny develop z:\plugins\airqualitymonitor\plugin.py
2. Make changes and save plugin.py
3. Restart Domoticz from a terminal: sudo service domoticz.sh restart
4. Wait a moment and refresh GUI > Log
5. Check the log and fix as required

!IMPORTANT!
In the **GUI > Setup > Settings**, enable accepting new hardware.
This is required to add the new hardware with its devices.

## Tinkerforge Master Brick and Bricklets
Ensure the Master Brick and Bricklets are running with the latest firmware.
To update, the Tinkerforge [Brick Viewer](https://www.tinkerforge.com/en/doc/Software/Brickv.html#brickv) is required.

For Tinkerforge development purposes installed the Brick Viewer and the required Brick Daemon on a Linux PC (called the piDevBook as running [Raspberry Pi Desktop](https://www.raspberrypi.org/downloads/raspberry-pi-desktop/).

**Steps to update the Master Brick and Bricklets**
1. Connect the Master Brick to the piDevBook using USB mini cable
2. Start the Brick Viewer (ensure to use the latest version)
3. Connect localhost:4223
4. Check if Master brickand Bricklets found
5. Select Update and check version differences
6. Update Master Brick
a. Button Erase - press and hold (DO NOT RELEASE)!
b. Button Reset - press and release
c. Button Erase - release!
The Master Brick Blue LED is turned off indicating boot mode.
7. The Brick Viewer shows only the Brick Tab
8. Refresh serial port = Serial Port: /dev/ttyACMo, Firmware: Master (2.4.10)
9. Flash
10. Master Brick reboots > Blue LED turns on and the Brick Viewer shows tabs Brick and Bricklets

See next Air Quality Prototype.

## Air Quality Monitor Prototype
Build the prototype by connecting the Tinkerforge Building Blocks (see hardware).
Connect the Master Brick to a device running the Brick Deamon and Viewer.
Just in a nutshell the actions taken to setup the Tinkerforge Building Blocks using the Tinkerforge Brick Viewer.
* Update the devices firmware
* Set the WiFi Master Extension fixed IP address in client mode
* Obtain the UID's of the Tinkerforge Bricklets as required by the Python plugin

After setting up the Tinkerforge Building Blocks, reset the Master Brick and check if the Master Brick can be reached via WLAN:
``` 
ping tf-wifi-ext-ip-address
``` 

## Domoticz Web UI's
Open windows GUI Setup > Hardware, GUI Setup > Log, GUI Setup > Devices
This is required to add the new hardware with its devices and monitor if the plugin code is running without errors.

## Create folder
```
cd /home/pi/domoticz/plugins/indoorairqualitymonitor
```

## Create the plugin
The plugin has a mandatory filename **plugin.py** located in the plugin folder /home/pi/domoticz/plugins/indoorairqualitymonitor.
For Python development Thonny, running on a Windows 10 device, is used.

Lookup for details in the source code **plugin.py** (well documented).

**Pseudo Code**
* INIT: set self vars to handle heartbeat count,ip connection state and UID list
* FIRST TIME: _onStart_ to create the Domoticz Devices and configure Tinkerforge Building Blocks
* NEXT TIME(S):
	*_onCommand_
		* Handle state changes
		* LCD Backlight on or off
	*_onHearbeat_
		* update LCD 20x4 display, RGB LED and Domoticz devices

The devices are manually added to the Domoticz Dashboard.
In addition a roomplan **Indoor Air Quality Monitor** is defined with all the IAQM devices and a simple floorplan using the roomplan.

## Restart Domoticz
Restart Domoticz to find the plugin:
```
sudo systemctl restart domoticz.service
```

**Note**
When making changes to the Python plugin code, ensure to restart Domoticz and refresh any of the Domoticz Web UI's.
This is the iteration process during development - build the solution step-by-step.

## Domoticz Add Hardware Air Quality Monitor
**IMPORTANT**
Prior adding, set GUI > Settings the option to allow new hardware.
If this option is not enabled, no new Air Quality device is created.
Check the GUI > Setup > Log as error message Python script at the line where the new device is used
(i.e. Domoticz.Debug("Device created: "+Devices[1].Name))

In the GUI > Setup > Hardware add the new hardware **Indoor Air Quality Monitor**.
The initial check interval is set at 60 seconds. This is a good value for testing, but for final version set to higher value like every 5 minutes (300 seconds).

## Add Hardware - Check the Domoticz Log
After adding,ensure to check the Domoticz Log (GUI > Setup > Log)
Example:
```
2019-06-09 10:08:23.075 Status: PluginSystem: Started, Python version '3.5.3'. 
2019-06-09 10:08:51.978 Status: (IAQM) Started. 
2019-06-09 10:08:52.743 (IAQM) Air Quality Monitor starting 
2019-06-09 10:08:52.743 (IAQM) Debug logging mask set to: PYTHON PLUGIN QUEUE IMAGE DEVICE CONNECTION MESSAGE ALL 
2019-06-09 10:08:52.743 (IAQM) 'Name':'IAQM' 
2019-06-09 10:08:52.743 (IAQM) 'Key':'IndoorAirQualityMonitor' 
2019-06-09 10:08:52.743 (IAQM) 'Version':'1.1.0 (Build 20190609)' 
2019-06-09 10:08:52.743 (IAQM) 'UserDataFolder':'/home/pi/domoticz/' 
2019-06-09 10:08:52.743 (IAQM) 'StartupFolder':'/home/pi/domoticz/' 
2019-06-09 10:08:52.743 (IAQM) 'Address':'192.168.1.114' 
2019-06-09 10:08:52.743 (IAQM) 'Mode5':'60' 
2019-06-09 10:08:52.743 (IAQM) 'Mode2':'60' 
2019-06-09 10:08:52.743 (IAQM) 'Language':'en' 
2019-06-09 10:08:52.743 (IAQM) 'Port':'4223' 
2019-06-09 10:08:52.743 (IAQM) 'Mode1':'6yLduG,Jvj,BHN,Jng,yyc' 
2019-06-09 10:08:52.743 (IAQM) 'DomoticzHash':'b06fb6b60' 
2019-06-09 10:08:52.743 (IAQM) 'HardwareID':'7' 
2019-06-09 10:08:52.743 (IAQM) 'Author':'rwbL' 
2019-06-09 10:08:52.744 (IAQM) 'Database':'/home/pi/domoticz/domoticz.db' 
2019-06-09 10:08:52.744 (IAQM) 'HomeFolder':'/home/pi/domoticz/plugins/indoorairqualitymonitor/' 
2019-06-09 10:08:52.744 (IAQM) 'Mode6':'Debug' 
2019-06-09 10:08:52.744 (IAQM) 'DomoticzBuildTime':'2019-06-08 15:28:08' 
2019-06-09 10:08:52.744 (IAQM) 'DomoticzVersion':'4.10881' 
2019-06-09 10:08:52.744 (IAQM) Device count: 0 
2019-06-09 10:08:52.744 (IAQM) Creating new devices ... 
2019-06-09 10:08:52.744 (IAQM) Creating device 'IAQ Index'. 
2019-06-09 10:08:52.745 (IAQM) Device created: IAQM - IAQ Index 
2019-06-09 10:08:52.745 (IAQM) Creating device 'IAQ Index Accuracy'. 
2019-06-09 10:08:52.746 (IAQM) Device created: IAQM - IAQ Index Accuracy 
2019-06-09 10:08:52.746 (IAQM) Creating device 'Air Quality'. 
2019-06-09 10:08:52.747 (IAQM) Device created: IAQM - Air Quality 
2019-06-09 10:08:52.747 (IAQM) Creating device 'Temperature'. 
2019-06-09 10:08:52.748 (IAQM) Device created: IAQM - Temperature 
2019-06-09 10:08:52.748 (IAQM) Creating device 'Humidity'. 
2019-06-09 10:08:52.749 (IAQM) Device created: IAQM - Humidity 
2019-06-09 10:08:52.749 (IAQM) Creating device 'Air Pressure'. 
2019-06-09 10:08:52.750 (IAQM) Device created: IAQM - Air Pressure 
2019-06-09 10:08:52.750 (IAQM) Creating device 'Ambient Light'. 
2019-06-09 10:08:52.751 (IAQM) Device created: IAQM - Ambient Light 
2019-06-09 10:08:52.751 (IAQM) Creating device 'LCD Backlight'. 
2019-06-09 10:08:52.752 (IAQM) Device created: IAQM - LCD Backlight 
2019-06-09 10:08:52.752 (IAQM) Creating device 'Status'. 
2019-06-09 10:08:52.753 (IAQM) Device created: IAQM - Status 
2019-06-09 10:08:52.753 (IAQM) Creating new devices: OK 
2019-06-09 10:08:52.753 (IAQM) UIDs:6yLduG,Jvj,BHN,Jng,yyc 
2019-06-09 10:08:52.753 (IAQM) SetMasterStatusLed - UID:6yLduG 
2019-06-09 10:08:52.762 (IAQM) Master Status LED disabled. 
2019-06-09 10:08:52.863 (IAQM) SetLCDBacklight - UID:BHN 
2019-06-09 10:08:52.872 (IAQM) LCD Backlight ON. 
2019-06-09 10:08:52.973 (IAQM - LCD Backlight) Updating device from 0:'' to have values 1:'0'. 
2019-06-09 10:08:52.981 (IAQM) SetLCDText - UID:BHN 
2019-06-09 10:08:52.740 Status: (IAQM) Entering work loop. 
2019-06-09 10:08:52.741 Status: (IAQM) Initialized version 1.1.0 (Build 20190609), author 'rwbL' 
2019-06-09 10:08:53.092 (IAQM) SetRGBLEDStatusLed - UID:Jng 
2019-06-09 10:08:53.103 (IAQM) RGB LED Status LED disabled. 
2019-06-09 10:08:53.204 (IAQM) ConfigAirQuality - UID:Jvj 
2019-06-09 10:08:53.212 (IAQM) Air Quality Status LED disabled. 
2019-06-09 10:08:53.313 (IAQM) Heartbeat set: 60 
2019-06-09 10:08:53.313 (IAQM) Pushing 'PollIntervalDirective' on to queue 
2019-06-09 10:08:53.313 (IAQM) Processing 'PollIntervalDirective' message 
2019-06-09 10:08:53.313 (IAQM) Heartbeat interval set to: 60. 
```

## Domoticz Log Entry IAQM Poll with Debug=True
The Indoor Air Quality Monitor runs every 60 seconds (Heartbeat interval) which is shown in the Domoticz log.
```
2019-06-09 19:12:25.236 (IAQM) Pushing 'onHeartbeatCallback' on to queue 
2019-06-09 19:12:25.260 (IAQM) Processing 'onHeartbeatCallback' message 
2019-06-09 19:12:25.262 (IAQM) Calling message handler 'onHeartbeat'. 
2019-06-09 19:12:25.262 (IAQM) onHeartbeat called. Counter=7380 (Heartbeat=60) 
2019-06-09 19:12:25.262 (IAQM) IP Connected created 
2019-06-09 19:12:25.264 (IAQM) Devices created - OK 
2019-06-09 19:12:25.275 (IAQM) IP Connection - OK 
2019-06-09 19:12:25.283 (IAQM - Index) Updating device from 0:'66' to have values 0:'75'. 
2019-06-09 19:12:25.288 (IAQM) IAQM - Index-IAQ Index:75 
2019-06-09 19:12:25.288 (IAQM - Index Accuracy) Updating device from 3:'Low' to have values 3:'Low'. 
2019-06-09 19:12:25.294 (IAQM) IAQM - Index Accuracy-IAQ IndexAccuracy:3,Low 
2019-06-09 19:12:25.294 (IAQM - Air Quality) Updating device from 2:'Moderate' to have values 2:'Moderate'. 
2019-06-09 19:12:25.299 (IAQM) Air Quality:2,Moderate 
2019-06-09 19:12:25.299 (IAQM - Temperature) Updating device from 0:'20' to have values 0:'20'. 
2019-06-09 19:12:25.303 (IAQM) IAQM - Temperature-Temperature:20 
2019-06-09 19:12:25.303 (IAQM - Humidity) Updating device from 47:'1' to have values 47:'1'. 
2019-06-09 19:12:25.306 (IAQM) IAQM - Humidity-Humidity:47 
2019-06-09 19:12:25.306 (IAQM - Air Pressure) Updating device from 0:'1021;0' to have values 0:'1021;0'. 
2019-06-09 19:12:25.310 (IAQM) IAQM - Air Pressure-Air Pressure:1021 
2019-06-09 19:12:25.310 (IAQM) Air Quality Devices updated 
2019-06-09 19:12:25.316 (IAQM - Ambient Light) Updating device from 0:'4' to have values 0:'4'. 
2019-06-09 19:12:25.319 (IAQM) IAQM - Ambient Light-Lux:4 
2019-06-09 19:12:25.319 (IAQM) Tinkerforge updating... 
2019-06-09 19:12:25.320 (IAQM) LCD Display cleared 
2019-06-09 19:12:25.322 (IAQM) LCD Lines written 
2019-06-09 19:12:25.322 (IAQM) RGB LED Color set 
2019-06-09 19:12:25.322 (IAQM - Status) Updating device from 0:'OK: 66,20,47,1021' to have values 0:'OK: 75,20,47,1021'. 
2019-06-09 19:12:25.328 (IAQM) OK: 75,20,47,1021 
2019-06-09 19:12:25.437 (IAQM) Update - OK.
```

## Custom Icon
A custom icon _Air Quality_ can be used for the _IAQ Index device_ (General,Custom Sensor).
To add the custom icon:
* Open GUI > Setup > More Options > Custom Icons
* Browse for the file _CustomIcons.zip_ and upload
* Select the IAQM Index widget > Edit > Sensor Icon > Select Air Quality > Update

## Custom Air Quality Level Parameter
The Air Quality parameter for the levels can be modified in the file **plugin.py**.
```
# Indoor Air Quality 1+6 Levels & Conditions & colors - see xml definition text
# The first (1) = 0 which is just a place holder to accomodate level array index 1 to 6
AIRQUALITYLEVELLIMIT = [0,50,100,150,200,300,500]
AIRQUALITYLEVELCONDITION = ["Unknown","Good","Moderate","Unhealthy Sensitive Groups","Unhealthy","Very Unhealthy","Hazardous"]
AIRQUALITYLEVELCOLOR = [[0,0,255],[0,255,0],[255,255,0],[255,165,0],[255,0,0],[128,0,128],[128,0,0]]
AIRQUALITYACCURACY = ["Unknown","High","Medium","Low","Unreliable"]
```

## Enhancements (dzVents Lua Scripts)
Sample enhancement scripts:
* **LCD Backlight**: turn OFF at 22:00 and ON at 07:00 (iaqm_lcd_backlight_control.lua).
* **Hue Light(s)**: Switch  ON | OFF depending Ambient Light Lux below or above threshold (iaqm_ambient_light_control.lua).

## Hints
* **Indoor Air Quality Station**: taking the power off and on again, update the IAQM hardware in Domoticz to init the Tinkerforge Building Blocks.
* **RGB LED**: Turn Off by setting the brightness to 0 (in Domoticz Web-UI Setup > Hardware).

## ToDo
See TODO.md
