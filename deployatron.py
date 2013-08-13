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
    'led_three'    : 7,
    'red'          : 2,
    'green'        : 3,
    'blue'         : 4
}

class LED():

    def __init__(self, name, pin, color_obj, color = 'BLACK'):
        self.name = name
        self.color_obj = color_obj
        self.last_color = color
        self.color = color
        self.pin = pin
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, GPIO.LOW)

    def activate(self, blink = False, delay = 0):
        if not (self.last_color is self.color):
            print "LED:" + self.name + "change to COLOR:" + self.color
            self.last_color = self.color
            self.color_obj.setColor(self.color)
        GPIO.output(self.pin, True)

    def deactivate(self):
        GPIO.output(self.pin, False)


class Switch():
    def __init__(self, pin):
        GPIO.setup(pin, GPIO.IN)

    def isActivated(self):
        pass

    pass

class Button():
    def __init__(self, pin):
        GPIO.setup(pin, GPIO.IN)

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
            #print ("setting pin:" + str(self.color_pins[i]) + " to pin:" + str(self.colors[color][i]))
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
    led_three = LED('led_three', pin_mapper['led_three'], color)

    #Group and pass the LEDs to our lighting thread
    led_array = [led_one, led_two, led_three]
    t = threading.Thread(target=threadLEDs, args = (led_array, 0.001))
    t.setDaemon(True)
    t.start()

    while True:
        led_one.color = Color.BLUE
        led_two.color = Color.GREEN
        led_three.color = Color.RED
        time.sleep(10)
        led_one.color = Color.WHITE
        led_two.color = Color.RED
        led_three.color = Color.WHITE
        time.sleep(10)

def threadLEDs(led_array, time_on):
    while True:
        for led in led_array:
            #print ("LED:" + led.name + " activating COLOR:" + led.color)
            led.activate()
            time.sleep(time_on)
            #print ("LED:" + led.name + " deactivating COLOR:" + led.color)
            led.deactivate()

main()
