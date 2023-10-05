from datetime import datetime, timezone
import RPi.GPIO as GPIO
import time

class Relay():
    def __init__(self,disable_warnings = True) -> None:
        # Default pins for the Waveshare Relay Hat (three relay version).
        self.One = 26
        self.Two = 20
        self.Three = 21

        if disable_warnings is True:
            GPIO.setwarnings(False)

        # By default, pins in the 0 state will flip a relay.
        # Setting the initial to 1 ensures they do not flip at start.
        GPIO.setmode(GPIO.BCM)

        self.initialize_relay(self.One)
        self.initialize_relay(self.Two)
        self.initialize_relay(self.Three)

    def initialize_relay(self,relay_pin: (int, getattr),
                         initial_pin_state: int = 1) -> None:
        """
        Initialize a relay at the given pin at a certain state.
        :param relay_pin: The GPIO pin that the relay sits on.
        :param initial_pin_state: The initial state of the pin.
        :return: None
        """
        GPIO.setup(relay_pin, GPIO.OUT, initial = initial_pin_state)

    def enable(self, relay_position: (int, getattr)) -> None:
        """
        Enable a relay. Success of this is visually indicated by a relay channel LED turning on.
        :param relay_position: An integer or an attribute of the Relay class. The pin for controlling the relay channel.
        :return: None
        """
        GPIO.output(relay_position, GPIO.LOW)
        time.sleep(0.01)

    def disable(self, relay_position: (int, getattr)) -> None:
        """
        Disable a relay. Success of this is visually indicated by a relay channel LED turning off.
        :param relay_position: An integer or an attribute of the Relay class. The pin for controlling the relay channel.
        :return: None
        """
        GPIO.output(relay_position, GPIO.HIGH)
        time.sleep(0.01)

    def state(self, relay_position: (int, getattr)) -> bool:
        """
        Obtain a relay state. If True, the relay is enabled. If False it is disabled. Relay state is opposite
        of pin state.
        :param relay_position: An integer or an attribute of the Relay class. The pin for controlling the relay channel.
        :return:
        """
        # dt = datetime.now(timezone.utc)
        dt = datetime.now()
        pin_state = bool(GPIO.input(relay_position))
        if pin_state is True:
            relay_state = False
        elif pin_state is False:
            relay_state = True
        return (dt, relay_state)

    def deinitialize(self) -> None:
        """
        Deinitialize everything and cleanup the pins.
        :return: None
        """
        GPIO.cleanup()

    def __enter__(self) -> object:
        """Context Manager. Allows for wrapping of the Relay() class into a with statement."""
        return self

    def __exit__(self,t,v,tb) -> None:
        """Context Manager. Allows for wrapping of the Relay() class into a with statement."""
        self.deinitialize()
