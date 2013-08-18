import RPi.GPIO as GPIO

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

            if self.blink == True:
                if self._countstate == 'on':
                    self._oncount = self._oncount + 1
                    if self._oncount == self.delay:
                        self._oncount = 0
                        self._countstate = 'off'
                    self.color_obj.setColor(self.color)
                elif self._countstate == 'off':
                    self._offcount = self._offcount + 1
                    if self._offcount == self.delay:
                        self._offcount = 0
                        self._countstate = 'on'
                    self.color_obj.setColor('BLACK')
                    return
            else:
                self.color_obj.setColor(self.color)

            GPIO.output(self.pin, True)

        else: pass
    #For calling from thread
    def _deactivate(self):
        #Give the RGB a moment to dim
        self.color_obj.setColor('BLACK')
        GPIO.output(self.pin, False)
