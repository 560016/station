import RPi.GPIO as GPIO
import time
from pynput import keyboard

# Define GPIO pins for stepper motor
PUL = 16  # Pulse pin
DIR = 19  # Direction pin
ENA = 14  # Enable pin

# Define GPIO pins for switches
switch_pins = [23, 24, 25, 26]

# Set GPIO mode
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Set up GPIO pins
GPIO.setup(PUL, GPIO.OUT)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(ENA, GPIO.OUT)

# Setup switch pins as inputs
for pin in switch_pins:
    GPIO.setup(pin, GPIO.IN)

# Enable motor driver
GPIO.output(ENA, GPIO.LOW)

# Number of steps per key press (increase this for larger movement)
STEP_COUNT = 100  

def read_switches():
    """Reads and prints the states of S1, S2, S3, S4"""
    S1 = GPIO.input(23)
    S2 = GPIO.input(24)
    S3 = GPIO.input(25)
    S4 = GPIO.input(26)
    print(f"S1: {S1}, S2: {S2}, S3: {S3}, S4: {S4}")

def step_motor(direction, steps=STEP_COUNT):
    """Moves the motor a given number of steps in the specified direction"""
    GPIO.output(DIR, direction)  # Set direction

    for _ in range(steps):
        GPIO.output(PUL, GPIO.HIGH)
        time.sleep(0.0005)  # Small delay for step pulse
        GPIO.output(PUL, GPIO.LOW)
        time.sleep(0.0005)  # Small delay
    
    read_switches()  # Read and print switch states after movement

def on_press(key):
    try:
        if key.char == 'a':
            print(f"Moving {STEP_COUNT} steps LEFT")
            step_motor(GPIO.LOW)

        elif key.char == 'd':
            print(f"Moving {STEP_COUNT} steps RIGHT")
            step_motor(GPIO.HIGH)

        elif key.char == 'q':
            print("Stopping motor... Exiting.")
            return False  # Stops the listener
    except AttributeError:
        pass

# Start listening for keyboard events
listener = keyboard.Listener(on_press=on_press)
listener.start()

print("Press 'A' to move left, 'D' to move right. Press 'Q' to quit.")

try:
    listener.join()  # Keeps the program running

except KeyboardInterrupt:
    print("\nStopping motor...")

finally:
    GPIO.output(ENA, GPIO.HIGH)  # Disable motor driver
    GPIO.cleanup()
