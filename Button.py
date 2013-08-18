import RPi.GPIO as GPIO

class Button():
    def __init__(self, name, pin, led = None):
        self.name = name
        self.led = led
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def onPress(self):
        pass