--[[
    iaqm_lcd_backlight_control.lua
    Switch the lcd backlight off at 2200 and on at 0700.
    Interpreter: dzVents, timer
    Author: Robert W.B. Linn
    Version: 20190610
]]--

-- idx of the devices
local IDX_LCDBACKLIGHT = 35    -- Type=Light/switch,Switch,On/Off

return {

	on = {
		timer = {
			'at 22:00',     -- OFF
			'at 07:00'      -- ON
		}
	},

	execute = function(domoticz, timer)
        if (timer.trigger == 'at 22:00') then
            domoticz.devices(IDX_LCDBACKLIGHT).switchOff()
        end
        if (timer.trigger == 'at 07:00') then
            domoticz.devices(IDX_LCDBACKLIGHT).switchOn()
        end
	end
}
