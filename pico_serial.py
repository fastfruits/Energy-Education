from machine import Pin
import time
import sys
import select

button1 = Pin(1, Pin.IN, Pin.PULL_DOWN)
button2 = Pin(2, Pin.IN, Pin.PULL_DOWN)
button3 = Pin(16, Pin.IN, Pin.PULL_DOWN)

led_red = Pin(4, Pin.OUT)
led_green = Pin(5, Pin.OUT)
led_blue = Pin(6, Pin.OUT)

def set_led(r, g, b):
    led_red.value(r)
    led_green.value(g)
    led_blue.value(b)

set_led(1, 0, 0)
time.sleep(0.5)
set_led(0, 0, 0)
while True:
    if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
        line = sys.stdin.readline().strip()
        
        if line == "LED1_RED":
            set_led(1, 0, 0)
        elif line == "LED1_GREEN":
            set_led(0, 1, 0)
        elif line == "LED1_WHITE":
            set_led(1, 1, 1)
        elif line == "LED1_OFF":
            set_led(0, 0, 0)
        
    if button1.value() == 1:
        print("BUTTON1_PRESSED")
        time.sleep(0.3)
    elif button2.value() == 1:
        print("BUTTON2_PRESSED")
        time.sleep(0.3)
    elif button3.value() == 1:
        print("BUTTON3_PRESSED")
        time.sleep(0.3)