### Status 20190608

#### UPD: Documentation Concept
Write up more details about the concept and the learnings. Use for the workbook  Domoticz Home Automation.
_Status_
Not started.

#### UPD: Domoticz Device AQM Index align with AQM Air Quality
Example: According Tinkerforge documentation is the Air Quality Average for an AQM Index of 84 ppm.
The Domoticz Device AQM states Excellent - would have expected Average. 
Need to check out the Domoticz documentation or source code for the rules / definition.
_Status_
Not started.

#### NEW: Push Buttons
Use the four LCD 20x4 Bricklet Push Buttons to extend functionality. 
Use the [Push Button Add-on](https://www.tinkerforge.com/en/shop/kits/weather-station-push-button-add-on.html) .
Functionality (to be reviewed):
* Button 1: Turn LCD backlight on/off
* Button 2: TBD
* Button 3: TBD
* Button 4: TBD
_Status_
Not started.

#### NEW: Control Hue light(s) if Illuminance below threshold
Either by using parameter Mode3 with idx1,idxN,threshold-level
or
dzVents script.
_Status_
Not started.

#### NEW: RGB LED use as Table Light
Kind of Hue color like - bit of soft color - use Domoticz Color switch  & On/Off switch..
_Status_
Not started.

#### NEW: IP Connection onStart & onStop
Instead of ip connect & disconnet for every heartbeat, use the function onStart to connect and onStop to disconnect.
This functionality is required for the push buttons callback.

#### NEW: Replace RGB LED by IO-$ with LED R-G-B.
Just an idea. Will probably drop.
_Status_
Not started.

#### NEW: Air Quality Level BAD or higher, RGB LED blinking.
Just an idea. Will probably drop.
Use API function set_status_led_config(config) with parameter STATUS_LED_CONFIG_SHOW_HEARTBEAT = 2
_Status_
Not started.
