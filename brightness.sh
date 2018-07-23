#/bin/bash
CURRENT_BRIGHTNESS=$(cat /sys/class/backlight/intel_backlight/brightness)
INCREASE_BRIGHTNESS=$(($CURRENT_BRIGHTNESS + 150))
DECREASE_BRIGHTNESS=$(($CURRENT_BRIGHTNESS - 150))
if [[ $1 == "1" ]]; then
	sudo tee /sys/class/backlight/intel_backlight/brightness <<< $INCREASE_BRIGHTNESS
elif [[ $1 == "0" ]]; then
	sudo tee /sys/class/backlight/intel_backlight/brightness <<< $DECREASE_BRIGHTNESS
fi
