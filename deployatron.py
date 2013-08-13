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
        self.color = color
        self.pin = pin
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, GPIO.LOW)

    def activate(self, blink = False, delay = 0):
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
        #@TODO for loop
        GPIO.output(self.color_pins[0], self.colors[color][0])
        GPIO.output(self.color_pins[1], self.colors[color][1])
        GPIO.output(self.color_pins[2], self.colors[color][2])

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
    GPIO.setmode(GPIO.BCM)
    color = Color(pin_mapper['red'], pin_mapper['green'], pin_mapper['blue'])
    led_one = LED('led_one', pin_mapper['led_one'], color)
    led_array = [led_one,]
    t = threading.Thread(target=threadLEDs, args = (led_array, 0.05))
    t.setDaemon(True)
    t.start()
    print "after thread"

    while True:
        led_one.color = Color.BLUE
        print ("Changed LED:" + led_one.name + " to COLOR:" + led_one.color)
        time.sleep(1)
        led_one.color = Color.RED
        print ("Changed LED:" + led_one.name + " to COLOR:" + led_one.color)
        time.sleep(1)

def threadLEDs(led_array, cycle_time):
    while True:
        for led in led_array:
            print ("LED:" + led.name + " activating COLOR:" + led.color)
            led.activate()
            time.sleep(cycle_time)
            print ("LED:" + led.name + " deactivating COLOR:" + led.color)
            led.deactivate()

main()
