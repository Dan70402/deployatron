__author__ = 'dan'
import RPi.GPIO as GPIO
import time
import threading
from Switch import Switch
from Color import Color
from Button import Button
from LED import LED

pin_mapper = {
    'master_key'   : 18,
    'switch_one'   : 23,
    'switch_two'   : 24,
    'switch_three' : 25,
    'big_red'      : 15,
    'led_one'      : 14,
    'led_two'      : 8,
    'led_three'    : 11,
    'led_four'     : 9,
    'red'          : 2,
    'green'        : 3,
    'blue'         : 4
}

def main():
    #Set board pin mode
    GPIO.setmode(GPIO.BCM)

    #Set RGB pins for RGB LEDs
    color = Color(pin_mapper['red'], pin_mapper['green'], pin_mapper['blue'])

    #Init our RGB LEDs
    led_one      = LED('led_one', pin_mapper['led_one'], color)
    led_two      = LED('led_two', pin_mapper['led_two'], color)
    led_three    = LED('led_three', pin_mapper['led_three'], color)
    led_four     = LED('led_four', pin_mapper['led_four'], color)
    master_key   = Switch('master_key', pin_mapper['master_key'])
    switch_one   = Switch('switch_one', pin_mapper['switch_one'])
    switch_two   = Switch('switch_two', pin_mapper['switch_two'])
    switch_three = Switch('switch_three', pin_mapper['switch_three'])
    big_red      = Button('big_red', pin_mapper['big_red'])

    #Group and pass the LEDs to our lighting thread
    led_array = [led_one, led_two, led_three, led_four]
    switch_array = [switch_one, switch_two, switch_three]
    t = threading.Thread(target=threadLEDs, args = (led_array, 0.01))
    t.setDaemon(True)
    t.start()


    #set switch off\on list
    sw_off_list = [master_key, switch_one, switch_two, switch_three]
    sw_on_list = []

    def remedySwitches():
        print "in remedy switches"
        #set switch off/on list
        sw_off_list = [switch_one, switch_two, switch_three]
        sw_on_list = [master_key]
        while not switchAllCheck(sw_off_list, sw_on_list):

            if not master_key.isActivated():
                for led in led_array:
                    print 'Master Key is not enabled.  Deactivating all the things'
                    led.deactivate()
            else:
                for switch in switch_array:
                    if switch.isActivated():
                        switch.led.color = Color.WHITE
                        switch.led.blink = False
                        switch.led.activate()
                    else:
                        switch.led.deactivate()

    def switchOnCheck(switch_on_list):

        sw_on_chk = None

        for switch in sw_on_list:
            if switch.isActivated():
                #We dont want to mark an existing True with a False
                if not sw_on_chk == False:
                    sw_on_chk = True
            else:
                sw_on_chk = False

        return sw_on_chk

    def switchOffCheck(switch_off_list):
        sw_off_chk = None

        for switch in sw_off_list:
            if switch.isActivated():
                sw_off_chk = False
            else:
                #We dont want to mark an existing False with a True
                if not sw_off_chk == False:
                    sw_off_chk = True

        return sw_off_chk

    def switchAllCheck(switch_off_list, switch_on_list):

        sw_chk = None
        sw_off_chk = switchOffCheck(sw_off_list)
        sw_on_chk = switchOnCheck(sw_on_list)

        for switch in sw_off_list:
            if (sw_off_chk == True) and (sw_on_chk == True):
                sw_chk = True
            else:
                print 'switch check failed'
                sw_chk = False

        return sw_chk



    while True:

        #On\Off Key
        if not switchAllCheck(sw_off_list, sw_on_list):
            remedySwitches()
        else:
            #Redundant right now #@TODO
            #set switch off\on list
            sw_off_list = [switch_one, switch_two, switch_three]
            sw_on_list = [master_key]

            #SW1
            if not switchAllCheck(sw_off_list, sw_on_list):
                remedySwitches()
            else:
                while not switchOnCheck():
                    if not switchOffCheck():
                        remedySwitches()
                    else:
                        #wiat for switch to come on
                        #turn on and blink led one
                        #turn off all other leds
                        pass
                #SW1 is on
                print 'activating sw1'
                #sw1 turn next color stage and still blink
                #Do stuff to verify stg1
                time.sleep(5)
                sw_off_list = [switch_two, switch_three]
                sw_on_list = [master_key, switch_one]
                #turn current led solid and blink next

                #SW2
                if not switchAllCheck(sw_off_list, sw_on_list):
                    remedySwitches()
                else:
                    while not switchOnCheck():
                        if not switchOffCheck():
                            remedySwitches()
                        else:
                            #wiat for switch to come on
                            #turn on and blink led one
                            #turn off all other leds
                            pass
                    #SW2 is on
                    print 'activating sw2'
                    #sw2 turn next color stage and still blink
                    #Do stuff to verify stg1
                    time.sleep(5)
                    sw_off_list = [switch_three]
                    sw_on_list = [master_key, switch_one, switch_two]
                    #turn current led solid and blink next

                    #SW3
                    if not switchAllCheck(sw_off_list, sw_on_list):
                        remedySwitches()
                    else:
                        while not switchOnCheck():
                            if not switchOffCheck():
                                remedySwitches()
                            else:
                                #wiat for switch to come on
                                #turn on and blink led one
                                #turn off all other leds
                                pass
                        #SW3 is on
                        print 'activating sw3'
                        #sw3 turn next color stage and still blink
                        #Do stuff to verify stg1
                        time.sleep(5)
                        sw_off_list = []
                        sw_on_list = [master_key, switch_one, switch_two, switch_three]
                        #turn current led solid and blink next

                    #Big Red


def threadLEDs(led_array, time_on):
    while True:
        for led in led_array:
            led._activate()
            time.sleep(time_on)
            led._deactivate()

try:
    main()
finally:
    GPIO.cleanup()