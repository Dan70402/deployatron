__author__ = 'dan'
import RPi.GPIO as GPIO
import time

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

    def __init__(self, pin, color_obj):
        self.color_obj = color_obj
        self.pin = pin
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, GPIO.LOW)

    def activate(self, blink = False, delay = 0):
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
        'BLUE'    : [ 0, 0, 1 ],
        'GREEN'   : [ 0, 1, 0 ],
        'CYAN'    : [ 0, 1, 1 ],
        'RED'     : [ 1, 0, 0 ],
        'MAGENTA' : [ 1, 0, 1 ],
        'YELLOW'  : [ 1, 1, 0 ],
        'WHITE'   : [ 1, 1, 1 ]
    }

    #Lookup vars
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

    while True:
        color.setColor(Color.BLUE)
        led_one = LED(pin_mapper['led_one'], color)
        led_one.activate()
        time.sleep(1)
        color.setColor(Color.RED)
        time.sleep(1)

main()
