from machine import Pin
class Button:
    def __init__(self,pin, callback=None, active_high=False, pull_resistor=True):
        self.button = Pin(pin, Pin.IN, Pin.PULL_UP)
        self.callback = callback
        self.last = self.state()
    
    def state(self):
        return not self.button.value()

    def proc(self):
        now=self.state()
        if self.last != now:
            self.last = now
            self.callback(now)