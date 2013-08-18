import RPi.GPIO as GPIO

class Switch():
    def __init__(self, name, pin, led = None):
        self.name = name
        self.pin = pin
        self.led = led
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def isActivated(self):
        isactive = GPIO.input(self.pin)
        return isactive