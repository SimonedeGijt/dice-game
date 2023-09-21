import RPi.GPIO as GPIO
import time
import logging

# Set the GPIO mode to BCM
GPIO.setmode(GPIO.BCM)

# Define the GPIO pin connected to the relay
relay_pin = 14  # Change this to the GPIO pin you're using

# Set up the GPIO pin as an output
GPIO.setup(relay_pin, GPIO.OUT)


def roll_dice():
    # Turn on the relay
    GPIO.output(relay_pin, GPIO.HIGH)
    logging.debug("Rolling a die")

    # Wait for 5 seconds
    time.sleep(2)

    # Turn off the relay
    GPIO.output(relay_pin, GPIO.LOW)
    logging.debug("Done rolling a die")
