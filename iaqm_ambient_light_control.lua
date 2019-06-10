--[[
    iaqm_ambient_light_control.lua
    Switch light(s) if the measued lux value isbelow threshold.
    Interpreter: dzVents, Device
    Author: Robert W.B. Linn
    Version: 20190610
]]--

local DOMOTICZURL = 'http://rpi-domoticz-ip:8080'
-- Parameter On | Off
local REQUESTURL = DOMOTICZURL .. '/json.htm?type=command&param=switchlight&idx=118&switchcmd='

-- idx of the devices
local IDX_AMBIENTLIGHT = 34    -- Type=Lux,Lux
local IDX_HUEMAKELAB = 118     -- Type=Light/Switch,Switch,Dimmer

-- threshold
local TH_AMBIENTLIGHT = 200

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
		domoticz.log('Device ' .. device.name .. ' was changed', domoticz.LOG_INFO)

        -- switch the Light On
		if domoticz.devices(IDX_AMBIENTLIGHT).lux <= TH_AMBIENTLIGHT and domoticz.data.lightstate == 0 then
            domoticz.openURL(REQUESTURL .. 'On')
            domoticz.data.lightstate = 1
		end

        -- switch the Light Off
		if domoticz.devices(IDX_AMBIENTLIGHT).lux > TH_AMBIENTLIGHT and domoticz.data.lightstate == 1 then
            domoticz.openURL(REQUESTURL .. 'Off')
            domoticz.data.lightstate = 0
		end

	end
}
