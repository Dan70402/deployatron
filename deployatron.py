__author__ = 'dan'
import RPi.GPIO as GPIO
import time
import threading


pin_mapper = {
    'switch_one'   : 18,
    'switch_two'   : 23,
    'switch_three' : 24,
    'button_one'   : 15,
    'led_one'      : 14,
    'led_two'      : 8,
    'led_three'    : 11,
    'red'          : 2,
    'green'        : 3,
    'blue'         : 4
}

class LED():

    def __init__(self, name, pin, color_obj, color = 'BLACK'):
        self.name = name
        self.color_obj = color_obj
        self.isactivated = None
        self.color = color
        self.pin = pin
        self.blink = False
        self.delay = 0
        self._countstate = 'off'
        self._offcount = 0
        self._oncount = 0
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, GPIO.LOW)

    #For calling to 'activate' (ie turn on) led in other thread from main thread
    def activate(self, blink = False, delay = 0):
        self.isactivated = True

    #For calling to 'activate' (ie turn on) led in other thread from main thread
    def deactivate(self, blink = False, delay = 0):
        self.isactivated = False

    #For calling from thread
    def _activate(self):
        if self.isactivated == True:

            if self.blink:
                if self._countstate == 'on':
                    self._oncount = self._oncount + 1
                    if self._oncount == self.delay:
                        self._oncount = 0
                        self._countstate = 'off'
                elif self._countstate == 'off':
                    self._offcount = self._offcount + 1
                    if self._offcount == self.delay:
                        self._offcount = 0
                        self._countstate = 'on'
                    return

            self.color_obj.setColor(self.color)
            GPIO.output(self.pin, True)
        else: pass
    #For calling from thread
    def _deactivate(self):
        #Give the RGB a moment to dim
        self.color_obj.setColor('BLACK')
        GPIO.output(self.pin, False)

class Switch():
    def __init__(self, pin):
        self.pin = pin
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def isActivated(self):
        isactive = GPIO.input(self.pin)
        return isactive

    pass

class Button():
    def __init__(self, pin):
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def onPress(self):
        pass

class Color():
    def __init__(self, red_pin, green_pin, blue_pin):
        self.color_pins = [red_pin, green_pin, blue_pin]
        for color_pin in self.color_pins:
            GPIO.setup(color_pin, GPIO.OUT)
            GPIO.output(color_pin, GPIO.LOW)

    def setColor(self, color):
        for i in xrange(len(self.color_pins)):
            GPIO.output(self.color_pins[i], self.colors[color][i])

    #RGB
    colors = {
        'BLACK'   : [ 0, 0, 0 ],
        'BLUE'    : [ 0, 0, 1 ],
        'GREEN'   : [ 0, 1, 0 ],
        'CYAN'    : [ 0, 1, 1 ],
        'RED'     : [ 1, 0, 0 ],
        'MAGENTA' : [ 1, 0, 1 ],
        'YELLOW'  : [ 1, 1, 0 ],
        'WHITE'   : [ 1, 1, 1 ]
    }

    #Lookup vars
    BLACK   = 'BLACK'
    BLUE    = 'BLUE'
    GREEN   = 'GREEN'
    CYAN    = 'CYAN'
    RED     = 'RED'
    MAGENTA = 'MAGENTA'
    YELLOW  = 'YELLOW'
    WHITE   = 'WHITE'

def main():
    #Set board pin mode
    GPIO.setmode(GPIO.BCM)

    #Set RGB pins for RGB LEDs
    color = Color(pin_mapper['red'], pin_mapper['green'], pin_mapper['blue'])

    #Init our RGB LEDs
    led_one   = LED('led_one', pin_mapper['led_one'], color)
    led_two   = LED('led_two', pin_mapper['led_two'], color)
    sw_one    = Switch(18)

    #Group and pass the LEDs to our lighting thread
    led_array = [led_one, led_two]
    t = threading.Thread(target=threadLEDs, args = (led_array, 0.001))
    t.setDaemon(True)
    t.start()

    led_one.activate()
    led_two.activate()


    while True:
        if sw_one.isActivated():
            led_one.color = Color.BLUE
            led_one.blink = True
            led_one.delay = 75

            led_two.color = Color.GREEN
            time.sleep(0.10)
        else:
            led_one.color = Color.RED
            led_one.blink = False
            led_two.color = Color.BLUE
            time.sleep(0.10)

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