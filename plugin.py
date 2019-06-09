# Domoticz Home Automation - Air Quality Monitor
# Monitor the Indoor Air Quality (IAQ) from the Tinkerforge Air Quality Bricklet, display on LCD 20x4 Display and indicate status on RGB LED.
# @author Robert W.B. Linn
# @version See plugin xml definition
#
# NOTE: after every change run
# sudo service domoticz.sh restart
# Domoticz Python Plugin Development Documentation:
# https://www.domoticz.com/wiki/Developing_a_Python_plugin


"""
<plugin key="IndoorAirQualityMonitor" name="Indoor Air Quality Monitor" author="rwbL" version="1.1.0 (Build 20190609)">
    <description>
        <h2>Indoor Air Quality Monitor v1.1.0</h2><br/>
        Measure the Indoor Air Quality (IAQ) Index (ppm), Condition and Accuracy, Air Pressure (mbar), Humidity (%), Temperature (C), Illuminance (lx).<br/>
		There are 6 IAQ Levels with range=condition (color):<br/>
		0-50=Good (green), 51-100=Moderate (yellow), 101-150=Unhealthy sensitive groups (orange), 151-200=Unhealthy (red), 201-300=Very Unhealthy (purple), 301-500=Hazardous (maroon).<br/>
		The IAQ Index Accuracy has 4 levels Unreliable, Low, Medium, High.
        <h3>Indoor Air Quality Station</h3>
        <ul style="list-style-type:square">
            <li>The Indoor Air Quality Station uses Tinkerforge Build Blocks Master Brick & WiFi Extension and Bricklets Air Quality, LCD 20x4 display, RGB LED, Ambient Light.</li>
            <li>LCD 20x4 display:</li>
            <ul>
                <li>Index ppm </li>
                <li>Air Quality Condition</li>
                <li>Temperature C, Humidity %, Air Pressure mbar, Illuminance lx</li>
            </ul>
            <li>RGB LED to indicate the Indoor Air Quality Level Color</li>
        </ul>
        <h3>Indoor Air Quality Devices (Type,SubType)</h3>
        <ul style="list-style-type:square">
            <li>Index (General,Custom Sensor), Index Accuracy (General,Alert), Air Quality (General, Alert [Text=Level]</li>
            <li>Temperature (Temp,LaCrosse TX3),Humidity (Humidity,LaCrosse TX3),Air Pressure (General,Barometer),Ambient Light (Lux,Lux)</li>
            <li>LCD Backlight (Light/Switch,Switch), Status (General,Text)</li>
        </ul>
        <h3>Configuration</h3>
        <ul style="list-style-type:square">
            <li>HTTP address and Port (default 4223) of the Master Brick WiFi Extension</li>
            <li>Tinkerforge UIDs as comma separated string (use Brick Viewer to determine): Master Brick; Bricklets: Air Quality, LCD 20x4, RGB LED, Ambient Light</li>
            <li>LED Brightness between 0 (off) and 100 (max)</li>
        </ul>
    </description>
    <params>
        <param field="Address" label="Host" width="200px" required="true" default="192.168.1.114"/>
        <param field="Port" label="Port" width="75px" required="true" default="4223"/>
        <param field="Mode1" label="UID (5)" width="200px" required="true" default="6yLduG,Jvj,BHN,Jng,yyc"/>
        <param field="Mode2" label="LED Brightness" width="75px" required="true" default="60"/>
        <param field="Mode5" label="Check Interval (sec)" width="75px" required="true" default="60"/>
        <param field="Mode6" label="Debug" width="75px">
            <options>
                <option label="True" value="Debug" default="true"/>
                <option label="False" value="Normal"/>
            </options>
        </param>
    </params>
</plugin>
""" 

# Set the plugin version which is displayon the LCD
PLUGINVERSION = "v1.1.0"

## Imports
import Domoticz
import urllib
import urllib.request

# Amend the import path to enable using the Tinkerforge libraries
# Alternate (ensure to update in case newer Python API bindings):
# create folder tinkerforge and copy the binding content, i.e.
# /home/pi/domoticz/plugins/soilmoisturemonitor/tinkerforge
from os import path
import sys
sys.path
sys.path.append('/usr/local/lib/python3.5/dist-packages')
                
import tinkerforge
from tinkerforge.ip_connection import IPConnection
from tinkerforge.brick_master import BrickMaster
from tinkerforge.bricklet_air_quality import BrickletAirQuality
from tinkerforge.bricklet_lcd_20x4 import BrickletLCD20x4
from tinkerforge.bricklet_rgb_led_v2 import BrickletRGBLEDV2
from tinkerforge.bricklet_ambient_light_v2 import BrickletAmbientLightV2

# Set RGB LED brightness level 0% (off) - 100% (brightest)
RGBBRIGHTNESS = 20
RGBBRIGHTNESSMIN = 0
RGBBRIGHTNESSMAX = 100

# Indoor Air Quality 1+6 Levels & Conditions & colors - see xml definition text
# The first (1) = 0 which is just a place holder to accomodate level array index 1 to 6
AIRQUALITYLEVELLIMIT = [0,50,100,150,200,300,500]
AIRQUALITYLEVELCONDITION = ["Unknown","Good","Moderate","Unhealthy Sensitive Groups","Unhealthy","Very Unhealthy","Hazardous"]
AIRQUALITYLEVELCOLOR = [[0,0,255],[0,255,0],[255,255,0],[255,165,0],[255,0,0],[128,0,128],[128,0,0]]
AIRQUALITYACCURACY = ["Unknown","High","Medium","Low","Unreliable"]

# Units of the device objects created by domoticz
# Syntax:UNIT<DomoticzTypeName><Function> - without blanks or underscores, function is optional
UNITMASTER = 0
UNITAIRQUALITYIAQINDEX = 1
UNITALERTIAQINDEXACCURACY = 2
UNITALERTAIRQUALITY = 3
UNITTEMPERATURE = 4
UNITHUMIDITY = 5
UNITBAROMETER = 6
UNITILLUMINATION = 7
UNITSWITCHBACKLIGHT = 8
UNITTEXTSTATUS = 9

# Index of the brick & bricklet uids from the UID list
# The uids are defined as a comma separated string in parameter Mode1
# Syntax:UIDINDEX<BrickBrickletName> - without blanks or underscores
UIDINDEXMASTER = 0
UIDINDEXAIRQUALITY = 1
UIDINDEXLCD = 2
UIDINDEXRGBLED = 3
UIDINDEXAMBIENTLIGHT = 4

class BasePlugin:
    
    def __init__(self):
        # The Domoticz heartbeat is set to every 60 seconds. Do not use a higher value as Domoticz message "Error: hardware (N) thread seems to have ended unexpectedly"
        # The Soil Moisture Monitor is read every Parameter.Mode5 seconds. This is determined by using a hearbeatcounter which is triggered by:
        # (self.HeartbeatCounter * self.HeartbeatInterval) % int(Parameter.Mode5) = 0
        self.HeartbeatInterval = 60
        self.HeartbeatCounter = 0
        # Flag to check if connected to the master brick
        self.ipConnected = 0
        # List of UIDs - Master Brick, Bricklet(s)
        self.UIDList = []
        return

    def onStart(self):
        Domoticz.Log("Air Quality Monitor starting")
        Domoticz.Debug("onStart called")
        Domoticz.Debug("Debug Mode:" + Parameters["Mode6"])
        
        if Parameters["Mode6"] == "Debug":
            self.debug = True
            Domoticz.Debugging(1)
            DumpConfigToLog()

        # if there no  devices, create these
        if (len(Devices) == 0):
            Domoticz.Debug("Creating new devices ...")

            # Index is a Custom Sensor as the Domoticz Air Quality Device is a Voltcraft which has different measures
            Options = {'Custom': '1;ppm'}
            Domoticz.Device(Name="Index", Unit=UNITAIRQUALITYIAQINDEX, TypeName="Custom", Subtype=31, Options=Options, Used=1).Create()
            Domoticz.Debug("Device created: "+Devices[UNITAIRQUALITYIAQINDEX].Name)

            Domoticz.Device(Name="Index Accuracy", Unit=UNITALERTIAQINDEXACCURACY, TypeName="Alert", Used=1).Create()
            Domoticz.Debug("Device created: "+Devices[UNITALERTIAQINDEXACCURACY].Name)
            
            Domoticz.Device(Name="Air Quality", Unit=UNITALERTAIRQUALITY, TypeName="Alert", Used=1).Create()
            Domoticz.Debug("Device created: "+Devices[UNITALERTAIRQUALITY].Name)
            
            Domoticz.Device(Name="Temperature", Unit=UNITTEMPERATURE, TypeName="Temperature", Used=1).Create()
            Domoticz.Debug("Device created: "+Devices[UNITTEMPERATURE].Name)
            
            Domoticz.Device(Name="Humidity", Unit=UNITHUMIDITY, TypeName="Humidity", Used=1).Create()
            Domoticz.Debug("Device created: "+Devices[UNITHUMIDITY].Name)
            
            Domoticz.Device(Name="Air Pressure", Unit=UNITBAROMETER, TypeName="Barometer", Used=1).Create()
            Domoticz.Debug("Device created: "+Devices[UNITBAROMETER].Name)
            
            Domoticz.Device(Name="Ambient Light", Unit=UNITILLUMINATION, TypeName="Illumination", Used=1).Create()
            Domoticz.Debug("Device created: "+Devices[UNITILLUMINATION].Name)
            
            Domoticz.Device(Name="LCD Backlight", Unit=UNITSWITCHBACKLIGHT, TypeName="Switch", Used=1).Create()
            Domoticz.Debug("Device created: "+Devices[UNITSWITCHBACKLIGHT].Name)
            
            # Control devices
            Domoticz.Device(Name="Status", Unit=UNITTEXTSTATUS, TypeName="Text", Used=1).Create()
            Domoticz.Debug("Device created: "+Devices[UNITTEXTSTATUS].Name)
            Domoticz.Debug("Creating new devices: OK")

        # Create the UID list using the UID as defined in the parameter Mode1
        ## The string contains multiple UIDs separated by comma (,). This enables to define more devices.
        UIDParam = Parameters["Mode1"]
        Domoticz.Debug("UIDs:" + UIDParam )
        ## Split the parameter string into a list of UIDs
        self.UIDList = UIDParam.split(',')
        # Check the list length (5 because 5 UIDs required, i.e. Master, Air Quality ...)
        if len(self.UIDList) < 5:
            Devices[UNITTEXTSTATUS].Update( nValue=0, sValue="[ERROR] UID parameter not correct! Should contain 5 UIDs." )
            Domoticz.Log(Devices[UNITTEXTSTATUS].sValue)

        # Master - Turn status led off
        SetMasterStatusLed(self, 0)

        # LCD - Turn backlight ON (Ensure to update the domoticz switch device),  set initial text.
        SetLCDBacklight(self, 'On')
        Devices[UNITSWITCHBACKLIGHT].Update( nValue=1, sValue=str(0))
        SetLCDText(self, "Indoor Air Quality", "Station " + PLUGINVERSION, "", "2019 by rwbl")

        # RGB LED - Turn status led off
        SetRGBLEDStatusLed(self, 0)

        # Air Quality - Turn status led off - NOT USED as replaced by ConfigAirQuality
        # SetAirQualityStatusLed(self, 0)
        # Air Quality - Config
        ConfigAirQuality(self)
    
        # Heartbeat
        Domoticz.Debug("Heartbeat set: "+Parameters["Mode5"])
        Domoticz.Heartbeat(self.HeartbeatInterval)

    def onStop(self):
        Domoticz.Debug("Plugin is stopping.")

    def onConnect(self, Connection, Status, Description):
        Domoticz.Debug("onConnect called")
        
    def onMessage(self, Connection, Data):
        Domoticz.Debug("onMessage called")

    def onCommand(self, Unit, Command, Level, Hue):
        Domoticz.Debug("onCommand called for Unit " + str(Unit) + ": Parameter '" + str(Command) + "', Level: " + str(Level))
        # LCD Backlight
        if Unit == UNITSWITCHBACKLIGHT:
            SetLCDBacklight(self, str(Command))
            if str(Command)=='On':
                Devices[UNITSWITCHBACKLIGHT].Update( nValue=1, sValue=str(Level))
            if str(Command)=='Off':
                Devices[UNITSWITCHBACKLIGHT].Update( nValue=0, sValue=str(Level))

    def onNotification(self, Name, Subject, Text, Status, Priority, Sound, ImageFile):
        Domoticz.Debug("Notification: " + Name + "," + Subject + "," + Text + "," + Status + "," + str(Priority) + "," + Sound + "," + ImageFile)

    def onDisconnect(self, Connection):
        Domoticz.Debug("onDisconnect called")

    def onHeartbeat(self):
        self.HeartbeatCounter = self.HeartbeatCounter + 1
        Domoticz.Debug("onHeartbeat called. Counter=" + str(self.HeartbeatCounter * self.HeartbeatInterval) + " (Heartbeat=" + Parameters["Mode5"] + ")")
        
        # Reset ipconnected flag
        self.ipConnected = 0

        # check the heartbeatcounter against the heartbeatinterval
        if (self.HeartbeatCounter * self.HeartbeatInterval) % int(Parameters["Mode5"]) == 0:

            try:
                
                # Create IP connection
                ipcon = IPConnection()
                Domoticz.Debug("IP Connected created")
                
                # Create the device objects
                master = BrickMaster(self.UIDList[UIDINDEXMASTER], ipcon)
                aq = BrickletAirQuality(self.UIDList[UIDINDEXAIRQUALITY], ipcon)
                lcd = BrickletLCD20x4(self.UIDList[UIDINDEXLCD], ipcon)
                rl = BrickletRGBLEDV2(self.UIDList[UIDINDEXRGBLED], ipcon) 
                al = BrickletAmbientLightV2(self.UIDList[UIDINDEXAMBIENTLIGHT], ipcon)
                Domoticz.Debug("Devices created - OK")

                # Connect to brickd using Host and Port
                try:
                    ipcon.connect(Parameters["Address"], int(Parameters["Port"]))
                    self.ipConnected = 1
                    Domoticz.Debug("IP Connection - OK")
                except:
                    Domoticz.Debug("[ERROR] IP Connection failed")

                # Don't use device before ipcon is connected

                # Set Alert Indicator to Orange with ERROR text
                if self.ipConnected == 0:
                    ## Alert device (5)nvalue=LEVEL - (0=gray, 1=green, 2=yellow, 3=orange, 4=red),svalue=TEXT
                    # Devices[ALERTDEVICE].Update( nValue=3, sValue="ERROR")
                    #Domoticz.Debug(Devices[ALERTDEVICE].Name + "-nValue=" + str(Devices[ALERTDEVICE].nValue) + ",sValue=" + Devices[ALERTDEVICE].sValue  )
                    Devices[UNITTEXTSTATUS].Update( nValue=0, sValue="[ERROR] Can not connect to the Master Brick. Check device or settings." )
                    Domoticz.Log(Devices[UNITTEXTSTATUS].sValue)
                    return

                # AIR QUALITY
                # Get current all values
                iaq_index, iaq_index_accuracy, temperature, humidity, air_pressure = aq.get_all_values()
                
                ## TESTdata with using the air quality bricklet
                '''
                iaq_index = 69 # 0 -200
                iaq_index_accuracy = 21
                temperature = 2432
                humidity = 6894
                air_pressure = 102412
                '''

                # Update the devices

                # IAQ (Indoor Air Quality) Index
                ## nValue=0
				## sValue=string value
                Devices[UNITAIRQUALITYIAQINDEX].Update( nValue=0,sValue=str(iaq_index) )
                # Devices[UNITAIRQUALITYIAQINDEX].Update( nValue=iaq_index, sValue="0")
                Domoticz.Debug(Devices[UNITAIRQUALITYIAQINDEX].Name + "-IAQ Index:" + str(iaq_index) )
 
                # IAQ Index Accuracy
                ## nvalue=LEVEL - (0=gray, 1=green, 2=yellow, 3=orange, 4=red)
                ## svalue=TEXT
                iaqaccuracylevel = 0
                if iaq_index_accuracy == aq.ACCURACY_UNRELIABLE:
                    iaqaccuracylevel = 4
                elif iaq_index_accuracy == aq.ACCURACY_LOW:
                    iaqaccuracylevel = 3
                elif iaq_index_accuracy == aq.ACCURACY_MEDIUM:
                    iaqaccuracylevel = 2
                elif iaq_index_accuracy == aq.ACCURACY_HIGH:
                    iaqaccuracylevel = 1
                iaqaccuracytext = AIRQUALITYACCURACY[iaqaccuracylevel]
                Devices[UNITALERTIAQINDEXACCURACY].Update( nValue=iaqaccuracylevel, sValue=iaqaccuracytext)
                Domoticz.Debug(Devices[UNITALERTIAQINDEXACCURACY].Name + "-IAQ IndexAccuracy:" + str(iaqaccuracylevel) + "," + iaqaccuracytext )

                # Air Quality
                ## nvalue=LEVEL - see xml definition
                ## svalue=TEXT
                airqualitylevel = 0
                if iaq_index >= 0 and iaq_index <= AIRQUALITYLEVELLIMIT[1]:
                    airqualitylevel = 1
                    
                if iaq_index > AIRQUALITYLEVELLIMIT[1] and iaq_index <= AIRQUALITYLEVELLIMIT[2]:
                    airqualitylevel = 2
                    
                if iaq_index > AIRQUALITYLEVELLIMIT[2] and iaq_index <= AIRQUALITYLEVELLIMIT[3]:
                    airqualitylevel = 3

                if iaq_index > AIRQUALITYLEVELLIMIT[3] and iaq_index <= AIRQUALITYLEVELLIMIT[4]:
                    airqualitylevel = 4

                if iaq_index > AIRQUALITYLEVELLIMIT[4] and iaq_index <= AIRQUALITYLEVELLIMIT[5]:
                    airqualitylevel = 5
                
                if iaq_index > AIRQUALITYLEVELLIMIT[5]:
                    airqualitylevel = 6

                airqualitytext = AIRQUALITYLEVELCONDITION[airqualitylevel]
                Devices[UNITALERTAIRQUALITY].Update( nValue=airqualitylevel, sValue=airqualitytext)
                Domoticz.Debug("Air Quality:" + str(airqualitylevel) + "," + airqualitytext  )

                # Temperature
                ## nvalue=0
                ## svalue=temperature/100
                ## print("Temperature: " + str(temperature/100.0) + " °C")
                if temperature > 0:
                    temperature = int(round(temperature/100.0))
                Devices[UNITTEMPERATURE].Update( nValue=0, sValue=str(temperature) )
                Domoticz.Debug(Devices[UNITTEMPERATURE].Name + "-Temperature:" + str(temperature) )

                # Humidity
                # nvalue=humidity
                # svalue=humiditystatus - 0=Normal,1=Comfortable,2=Dry,3=Wet
                # print("Humidity: " + str(humidity/100.0) + " %RH")
                if humidity > 0:
                    humidity = int(round(humidity /100.0))
                humiditystatus=GetHumidityStatus(humidity)
                Devices[UNITHUMIDITY].Update( nValue=humidity, sValue=str(humiditystatus) )
                Domoticz.Debug(Devices[UNITHUMIDITY].Name + "-Humidity:" + str(humidity) )

                # Air Pressure
                # nvalue=0
                # svalue=airpressure/100;prediction
                # print("Air Pressure: " + str(air_pressure/100.0) + " mbar")
                if air_pressure > 0:
                    air_pressure = int(round(air_pressure /100.0))
                Devices[UNITBAROMETER].Update( nValue=0, sValue=str(air_pressure) + ";0" )
                Domoticz.Debug(Devices[UNITBAROMETER].Name + "-Air Pressure:" + str(air_pressure) )

                Domoticz.Debug("Air Quality Devices updated")

                # AMBIENT LIGHT
                ## Get current illuminance
                ## nvalue=0
                ## svalue=illuminance/100
                illuminance = al.get_illuminance()
                if illuminance > 0:
                    illuminance = int(round(illuminance/100.0))
                #print("Illuminance: " + str(illuminance/100.0) + " lx")
                Devices[UNITILLUMINATION].Update( nValue=0, sValue=str(illuminance) )
                Domoticz.Debug(Devices[UNITILLUMINATION].Name + "-Lux:" + str(illuminance) )

                #
                ## Tinkerforge Bricklet Updates
                #
                Domoticz.Debug("Tinkerforge updating..." )

                ## LCD Display
                ## Writes text to a specific line (0 to 3) with a specific position (0 to 19). The text can have a maximum of 20 characters.
                
                ## Turn backlight on NOTE: done in onStart
                ## lcd.backlight_on()
                ## Domoticz.Debug("LCD Backlight ON")

                ## Clear the display
                lcd.clear_display()
                Domoticz.Debug("LCD Display cleared")

                ## Get the values as strings to write on the lcd
                ## AQI
                lcdaqi = str(iaq_index)

                ## TT:HH - TT=Temperature,HH=Humidity
                lcdtemperature = str(temperature)
                lcdhumidity = "HH"
                if humidity < 100:
                    lcdhumidity = str(humidity)

                ## airpressure
                lcdairpressure = str(air_pressure)

                ## illuminance
                lcdilluminance = str(illuminance)
                
                ## write to the lcd: line (int,0-3),pos(int,0-19),text
                lcd.write_line(0, 0, "Q: " + lcdaqi + " ppm " + airqualitytext)
                lcd.write_line(1, 0, "T: " + lcdtemperature + " C")
                lcd.write_line(1, 14, "H: " + lcdhumidity + "%")
                lcd.write_line(2, 0, "P: " + lcdairpressure + " mbar")
                lcd.write_line(3, 0, "L: " + lcdilluminance + " lx")
                lcd.write_line(3, 14, PLUGINVERSION)
                Domoticz.Debug("LCD Lines written")

                ## rgb led set color depending indoor air quality index
                ## Set the brightness using the value of the parameter Mode2
                lbbrightness = int(Parameters["Mode2"])
                if lbbrightness < RGBBRIGHTNESSMIN:
                    lbbrightness = RGBBRIGHTNESSMIN
                if lbbrightness > RGBBRIGHTNESSMAX:
                    lbbrightness = RGBBRIGHTNESSMAX

                rl.set_rgb_value(SetRGBColor(AIRQUALITYLEVELCOLOR[airqualitylevel][0],lbbrightness), SetRGBColor(AIRQUALITYLEVELCOLOR[airqualitylevel][1],lbbrightness), SetRGBColor(AIRQUALITYLEVELCOLOR[airqualitylevel][2],lbbrightness))
                Domoticz.Debug("RGB LED Color set")

                # Log Message
                Devices[UNITTEXTSTATUS].Update( nValue=0, sValue="OK: " + lcdaqi + ","+ lcdtemperature + "," + lcdhumidity + "," + lcdairpressure)
                Domoticz.Log(Devices[UNITTEXTSTATUS].sValue)

                # Disconnect
                ipcon.disconnect()

                # Log Message
                Domoticz.Debug("Update - OK.")
                
            except:
                # Error
                # Important to close the connection - if not, the plugin can not be disabled
                if self.ipConnected == 1:
                    ipcon.disconnect()
            
                Devices[UNITTEXTSTATUS].Update( nValue=0, sValue="[ERROR] Check settings, correct and restart Domoticz." )
                Domoticz.Log(Devices[UNITTEXTSTATUS].sValue)
                
global _plugin
_plugin = BasePlugin()

def onStart():
    global _plugin
    _plugin.onStart()

def onStop():
    global _plugin
    _plugin.onStop()

def onConnect(Connection, Status, Description):
    global _plugin
    _plugin.onConnect(Connection, Status, Description)

def onMessage(Connection, Data):
    global _plugin
    _plugin.onMessage(Connection, Data)

def onCommand(Unit, Command, Level, Hue):
    global _plugin
    _plugin.onCommand(Unit, Command, Level, Hue)

def onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile):
    global _plugin
    _plugin.onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile)

def onDisconnect(Connection):
    global _plugin
    _plugin.onDisconnect(Connection)

def onHeartbeat():
    global _plugin
    _plugin.onHeartbeat()

# Generic helper functions
def DumpConfigToLog():
    for x in Parameters:
        if Parameters[x] != "":
            Domoticz.Debug( "'" + x + "':'" + str(Parameters[x]) + "'")
    Domoticz.Debug("Device count: " + str(len(Devices)))
    for x in Devices:
        Domoticz.Debug("Device:           " + str(x) + " - " + str(Devices[x]))
        Domoticz.Debug("Device ID:       '" + str(Devices[x].ID) + "'")
        Domoticz.Debug("Device Name:     '" + Devices[x].Name + "'")
        Domoticz.Debug("Device nValue:    " + str(Devices[x].nValue))
        Domoticz.Debug("Device sValue:   '" + Devices[x].sValue + "'")
        Domoticz.Debug("Device LastLevel: " + str(Devices[x].LastLevel))
    return

# Get humiditystatus - 0=Normal,1=Comfortable,2=Dry,3=Wet
# Return 0=Normal,1=Comfortable,2=Dry,3=Wet
def GetHumidityStatus(Humidity):
    if (Humidity < 25):
        return 2
    if (Humidity > 60):
        return 3
    if ((Humidity >= 25) and (Humidity <= 60)):
        return 1
    return 0

# Master - Set the status led
# state = 0 (OFF) | 1 (ON)
def SetMasterStatusLed(self, state):
    Domoticz.Debug("SetMasterStatusLed - UID:" + self.UIDList[UIDINDEXMASTER])
    try:
        # Create IP connection
        ipcon = IPConnection() 
        # Create device object
        master = BrickMaster(self.UIDList[UIDINDEXMASTER], ipcon)
        # Connect to brickd
        ipcon.connect(Parameters["Address"], int(Parameters["Port"]))
        # Don't use device before ipcon is connected
        if state == 0:
            master.disable_status_led()
            Domoticz.Log("Master Status LED disabled.")

        if state == 1:
            master.enable_status_led()
            Domoticz.Log("Master Status LED enabled.")

        ipcon.disconnect()
        
        return 1

    except:
        # Error
        Domoticz.Log("[ERROR] Can not set Master Status LED.")
        return 0

# RGB LED - Set the status led
# state = 0 (OFF) | 1 (ON) | 2 (show heartbeat) | 3 (show status)
def SetRGBLEDStatusLed(self, state):
    Domoticz.Debug("SetRGBLEDStatusLed - UID:" + self.UIDList[UIDINDEXRGBLED])
    try:
        # Create IP connection
        ipcon = IPConnection() 
        # Create device object
        rl = BrickletRGBLEDV2(self.UIDList[UIDINDEXRGBLED], ipcon) 
        # Connect to brickd
        ipcon.connect(Parameters["Address"], int(Parameters["Port"]))
        # Don't use device before ipcon is connected
        if state == 0:
            rl.set_status_led_config(state)
            Domoticz.Log("RGB LED Status LED disabled.")

        if state == 1:
            rl.set_status_led_config(state)
            Domoticz.Log("RGB LED Status LED enabled.")

        ipcon.disconnect()
        
        return 1

    except:
        # Error
        Domoticz.Log("[ERROR] Can not set RGB LED Status LED.")
        return 0

# Set the rgb color adjusted
def SetRGBColor(color, brightness):
    newcolor = 0
    if (brightness > 0) and (color > 0):
        newcolor = int(color * brightness  / 100)
    return newcolor

# Air Quality - Set the status led
# state = 0 (OFF) | 1 (ON) | 2 (show heartbeat) | 3 (show status)
def SetAirQualityStatusLed(self, state):
    Domoticz.Debug("SetAirQualityStatusLed - UID:" + self.UIDList[UIDINDEXAIRQUALITY])
    try:
        # Create IP connection
        ipcon = IPConnection() 
        # Create device object
        aq = BrickletAirQuality(self.UIDList[UIDINDEXAIRQUALITY], ipcon)
        # Connect to brickd
        ipcon.connect(Parameters["Address"], int(Parameters["Port"]))
        # Don't use device before ipcon is connected
        if state == 0:
            aq.set_status_led_config(state)
            Domoticz.Log("Air Quality Status LED disabled.")

        if state == 1:
            aq.set_status_led_config(state)
            Domoticz.Log("Air Quality Status LED enabled.")

        ipcon.disconnect()
        
        return 1

    except:
        # Error
        Domoticz.Log("[ERROR] Can not set Air Quality Status LED.")
        return 0

# Air Quality - Config
# Various configuration settings:
# Set the status led - state = 0 (OFF) | 1 (ON) | 2 (show heartbeat) | 3 (show status)
def ConfigAirQuality(self):
    Domoticz.Debug("ConfigAirQuality - UID:" + self.UIDList[UIDINDEXAIRQUALITY])
    try:
        # Create IP connection
        ipcon = IPConnection() 
        # Create device object
        aq = BrickletAirQuality(self.UIDList[UIDINDEXAIRQUALITY], ipcon)
        # Connect to brickd
        ipcon.connect(Parameters["Address"], int(Parameters["Port"]))
        # Don't use device before ipcon is connected

        # Turn off status led
        aq.set_status_led_config(0)
        Domoticz.Log("Air Quality Status LED disabled.")

        # Set temperature offset with resolution 1/100°C. Offset 10 = decrease measured temperature by 0.1°C, 100 = 1°C.
        # offset - int
        # Test with 2°C = 200
        aq.set_temperature_offset(200)

        # The Air Quality Bricklet uses an automatic background calibration mechanism to calculate the IAQ Index.
        # This calibration mechanism considers a history of measured data. Duration history = 4 days (0) or 28 days (1).
        # duration - int 0 | 1
        # Test with 0 = 4 days
        aq.set_background_calibration_duration(0)

        ipcon.disconnect()
        
        return 1

    except:
        # Error
        Domoticz.Log("[ERROR] Can not set Air Quality Status LED.")
        return 0

# Turn the LCD backlight on or off
# state = 'On' | 'Off'
def SetLCDBacklight(self, state):
    Domoticz.Debug("SetLCDBacklight - UID:" + self.UIDList[UIDINDEXLCD])
    try:
        # Create IP connection
        ipcon = IPConnection() 
        # Create device object
        lcd = BrickletLCD20x4(self.UIDList[UIDINDEXLCD], ipcon)
        # Connect to brickd
        ipcon.connect(Parameters["Address"], int(Parameters["Port"]))
        # Don't use device before ipcon is connected
        if state == 'Off':
            lcd.backlight_off()
            Domoticz.Log("LCD Backlight OFF.")

        if state == 'On':
            lcd.backlight_on()
            Domoticz.Log("LCD Backlight ON.")

        ipcon.disconnect()
        
        return 1

    except:
        # Error
        Domoticz.Log("[ERROR] Can not set Master Status LED.")
        return 0
        
# Set the LCD text by writing up to 4 lines starting at pos 0
# line1,line2,line3,line4
def SetLCDText(self, line1, line2, line3, line4):
    Domoticz.Debug("SetLCDText - UID:" + self.UIDList[UIDINDEXLCD])
    try:
        # Create IP connection
        ipcon = IPConnection() 
        # Create device object
        lcd = BrickletLCD20x4(self.UIDList[UIDINDEXLCD], ipcon)
        # Connect to brickd
        ipcon.connect(Parameters["Address"], int(Parameters["Port"]))
        # Don't use device before ipcon is connected
        ## write to the lcd: line (int,0-3),pos(int,0-19),text
        lcd.clear_display()
        lcd.write_line(0, 0, line1)
        lcd.write_line(1, 0, line2)
        lcd.write_line(2, 0, line3)
        lcd.write_line(3, 0, line4)

        ipcon.disconnect()
        
        return 1

    except:
        # Error
        Domoticz.Log("[ERROR] Can not set Master Status LED.")
        return 0
        
