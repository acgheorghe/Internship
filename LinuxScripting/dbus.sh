#!/bin/bash


monitor_power_changes(){
        dbus-send --print-reply --system --dest=org.freedesktop.UPower /org/freedesktop/UPower/devices/battery_BAT0 org.freedesktop.DBus.Properties.Get string:org.freedesktop.UPower.Device string:State |
        grep variant |
        while read -r variant type value; do
              #return $value
              echo $value
        done
}


get_power_status(){
        # works for return in the previous function
        #monitor_power_changes > /dev/null
        #charging_status=$?
        charging_status=$(monitor_power_changes)

        if [ "$charging_status" == "1" ]; then
                echo "This machine is currently charging!"

        elif [ "$charging_status" == "2" ]; then
                echo "This machine is currently using battery!"
        else
                echo "Unable to determine the state"
        fi

}

get_power_status
