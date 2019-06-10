--[[
    iaqm_ambient_light_control.lua
    Switch light(s) if the measued lux value is below threshold.
    The threshold is set by the user variable TH_IAQM_AMBIENTLIGHT - idx=1, type=Integer,value=100 (or other)
    This example runs on a Domoticz development server and switches a Hue light (idx=118) on the Domoticz production server via HTTP API request.
    Interpreter: dzVents, Device
    Author: Robert W.B. Linn
    Version: 20190610
]]--

local DOMOTICZURL = 'http://rpi-domoticz-ip:8080'
-- Parameter On | Off
local REQUESTURL = DOMOTICZURL .. '/json.htm?type=command&param=switchlight&idx=118&switchcmd='

-- NOT USED for now
-- ensure the httpResponse name is unique across all dzVents scripts! use the scriptname plus Callback
local HTTPCALLBACKNAME = 'IAQMAmbientLightControlCallback'

-- idx of the devices
local IDX_AMBIENTLIGHT = 34         -- Type=Lux,Lux
local IDX_HUEMAKELAB = 118          -- Type=Light/Switch,Switch,Dimmer

-- idx of the user variables (TH = Threshold)
local IDX_TH_IAQM_AMBIENTLIGHT = 1  -- Type:Integer

return {
	on = {
		devices = {
			IDX_AMBIENTLIGHT
		}
	},
    data = {
        -- keep the light state
        lightstate = { initial = 0 }
   },

	execute = function(domoticz, device)
		-- domoticz.log('Device ' .. device.name .. ' was changed', domoticz.LOG_INFO)

        -- get the threshold from the user variable
        local threshold = domoticz.variables(IDX_TH_IAQM_AMBIENTLIGHT).value

        -- switch light if the threshold > 0
        if threshold > 0 then
            -- switch the Light On
	    	if domoticz.devices(IDX_AMBIENTLIGHT).lux <= threshold and domoticz.data.lightstate == 0 then
                domoticz.openURL(REQUESTURL .. 'On')
                domoticz.data.lightstate = 1
    		end

            -- switch the Light Off
		    if domoticz.devices(IDX_AMBIENTLIGHT).lux > threshold and domoticz.data.lightstate == 1 then
                domoticz.openURL(REQUESTURL .. 'Off')
                domoticz.data.lightstate = 0
		    end
            
        end

	end
}
