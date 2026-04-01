from machine import Pin
import time
import sys

button1 = Pin(1, Pin.IN, Pin.PULL_DOWN)
button2 = Pin(2, Pin.IN, Pin.PULL_DOWN)
button3 = Pin(3, Pin.IN, Pin.PULL_DOWN)

led1 = Pin(4, Pin.OUT)
led2 = Pin(5, Pin.OUT)
led3 = Pin(6, Pin.OUT)

while True:
    if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
        line = sys.stdin.readline().strip()
        
        if line == "LED_ON":
            led.value(1)
        elif line == "LED_OFF":
            led.value(0)
        
        if button1.value() == 1:
            print("BUTTON1_PRESSED", flush=True)
            time.sleep(0.3)
        elif button2.value() == 1:
            print("BUTTON1_PRESSED", flush=True)
            time.sleep(0.3)
        elif button3.value() == 1:
            print("BUTTON1_PRESSED", flush=True)
            time.sleep(0.3)
        