import serial
import threading
import time

ser = None

try:
    ser = serial.Serial('/dev/tty.usbmodem1301', 9600, timeout=1)
    print("Connected to pico")
except Exception:
    print("No pico to connect to! CHECK PORT")

button1_pressed = False
button2_pressed = False
button3_pressed = False

def listen():
    global button1_pressed
    global button2_pressed
    global button3_pressed
    
    while True:
        if ser is None:
            time.sleep(0.1)
            continue
        
        try:
            line = ser.readline().decode('utf-8').strip()

            if line == "BUTTON1_PRESSED":
                button1_pressed = True

            elif line == "BUTTON2_PRESSED":
                button2_pressed = True

            elif line == "BUTTON3_PRESSED":
                button3_pressed = True

        except Exception as e:
            print(f"Error reading serial port {e}")
            time.sleep(0.1)

thread = threading.Thread(target=listen, daemon=True)
thread.start()


# Repeat this function for each led
def send_led1_status(color):
    if color == "white":
        ser.write(b"LED1_WHITE\n")
    elif color == "red":
        ser.write(b"LED1_RED\n")
    elif color == "green":
        ser.write(b"LED1_GREEN\n")

