import RPi.GPIO as GPIO
import time

# Set the GPIO mode to BCM
GPIO.setmode(GPIO.BCM)

# Define the GPIO pin connected to the relay
relay_pin = 14  # Change this to the GPIO pin you're using

# Set up the GPIO pin as an output
GPIO.setup(relay_pin, GPIO.OUT)


def roll_dice():
    # Turn on the relay
    GPIO.output(relay_pin, GPIO.HIGH)
    print("Rolling a die")

    # Wait for 5 seconds
    time.sleep(2)

    # Turn off the relay
    GPIO.output(relay_pin, GPIO.LOW)
    print("Done rolling a die")
