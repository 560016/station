import RPi.GPIO as GPIO
import time

# GPIO Pin Assignments
PUL = 16  # Motor Clock
DIR = 19  # Motor Direction
ENA = 14  # Motor Enable

S1 = 23  # Carrier Sensors (Active Low)
S2 = 24
S3 = 25
S4 = 26

P1 = 4   # Position Sensors (Active Low)
P2 = 17
P3 = 27
P4 = 22

# Stepper Motor Control Constants
STEP_DELAY = 0.0005  # Adjust step delay for speed
STEP_COUNT = 5       # Steps per loop iteration (increase for faster motion)

# GPIO Setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Configure GPIOs
for pin in [PUL, DIR, ENA]:
    GPIO.setup(pin, GPIO.OUT)

for pin in [S1, S2, S3, S4, P1, P2, P3, P4]:
    GPIO.setup(pin, GPIO.IN)

# Enable Motor
GPIO.output(ENA, GPIO.LOW)

def move_motor(direction, stop_sensor):
    """ Moves the motor in a given direction until a sensor goes LOW """
    GPIO.output(DIR, direction)
    while GPIO.input(stop_sensor) == GPIO.HIGH:  # Wait until sensor goes LOW
        for _ in range(STEP_COUNT):
            GPIO.output(PUL, GPIO.HIGH)
            time.sleep(STEP_DELAY)
            GPIO.output(PUL, GPIO.LOW)
            time.sleep(STEP_DELAY)
    time.sleep(0.1)  # Small delay to stabilize sensor reading

def send_capsule():
    """ Implements the SEND sequence """
    print("Send process started")
    
    # Wait for P1 to be LOW (Capsule Ready)
    while GPIO.input(P1) == GPIO.LOW:
        pass
    print("Capsule detected at P1")

    # Move motor right until S4 goes LOW (Drop Position)
    move_motor(GPIO.LOW, S4)
    print("Capsule dropped")

    # Wait for P1 to go HIGH and P2 to go LOW (Capsule Moved)
    while GPIO.input(P1) == GPIO.HIGH or GPIO.input(P2) == GPIO.LOW:
        pass
    print("Capsule moved to P2 position")

    # Move motor left until S2 goes LOW
    move_motor(GPIO.HIGH, S2)

    # Check for P3, if LOW, turn blower ON
    if GPIO.input(P3) == GPIO.LOW:
        print("Blower ON")
        
    print("......")
    time.sleep(10)
    print("Package sent")

    # Move motor left until S2 is LOW to return to pass-through state
    move_motor(GPIO.LOW, S2)
    print("System reset to pass-through state")

def receive_capsule():
    """ Implements the RECEIVE sequence """
    print("Receive process started")
    
    # Wait for P3 to go LOW (Package Incoming)
    while GPIO.input(P3) == GPIO.LOW:
        print("hello")
        move_motor(GPIO.HIGH, S3)
    
    '''if GPIO.input(P3) == GPIO.LOW:
        move_motor(GPIO.HIGH, S3)
    else:
        pass'''
    print("SUCTION HIGH - Capsule Picked")
    
    # Wait for P4 to go LOW
    #while GPIO.input(P4) == GPIO.HIGH:
     #   pass

    # Move motor left until S1 goes LOW
    if GPIO.input(P4) == GPIO.LOW:
        move_motor(GPIO.LOW, S4)
    else:
        pass

    print("Package received")
    move_motor(GPIO.HIGH, S2)
    print("System reset to pass-through state")

def main():
    """ Main loop to process user input """
    while True:
        print("\nEnter 1 to SEND, 2 to RECEIVE, Q to Quit:")
        choice = input().strip()
        
        if choice == '1':
            send_capsule()
        elif choice == '2':
            receive_capsule()
        elif choice.lower() == 'q':
            print("Exiting system...")
            break
        else:
            print("Invalid input! Please enter 1, 2, or Q.")

try:
    main()
except KeyboardInterrupt:
    print("\nStopping system...")
finally:
    GPIO.output(ENA, GPIO.HIGH)  # Disable motor
    GPIO.cleanup()
