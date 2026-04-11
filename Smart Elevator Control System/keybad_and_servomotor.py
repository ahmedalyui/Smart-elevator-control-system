import RPi.GPIO as GPIO
import time
import drivers  ##
from pad4pi import rpi_gpio

KEYPAD = [
    [1, 2, 3, "A"],
    [4, 5, 6, "B"],
    [7, 8, 9, "C"],
    ["*", 0, "#", "D"]
]

ROW_PINS = [17, 27, 22, 5]  # BCM numbering
COL_PINS = [23, 24, 25, 16]  # BCM numbering

# setup RPi
GPIO.setwarnings(False)

# setup servo config
servo_pin = 12

GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin, GPIO.OUT)

pwm = GPIO.PWM(servo_pin, 50)
pwm.start(0)

display = drivers.Lcd()  ##

DEFAULT_INDENT = "     "

input_key_codes = DEFAULT_INDENT

DEFAULT_KEYCODE_LENGTH = 6


def open_lock():
    print("Opening lock ... ")
    pwm.ChangeDutyCycle(11)

    time.sleep(5)

    print("Closing lock after 5 secs ... ")

    close_lock()

    pwm.ChangeDutyCycle(0)


def close_lock():
    print("Closing lock ... ")

    pwm.ChangeDutyCycle(2)

    time.sleep(1)


def cleanup():
    pwm.stop()
    GPIO.cleanup()
    display.lcd_clear()  ##

    print("Releasing resources and stopping our Program ... ")


def display_to_lcd(data, position=2, show_input_keycode=False, duration=1):  ##
    display.lcd_clear()

    if show_input_keycode:
        display.lcd_display_string("Input Keycode:", 1)
        display.lcd_display_string(input_key_codes, 2)

    time.sleep(0.1)

    if data is not None:
        display.lcd_display_string(data, position)

    if duration is not None:
        time.sleep(duration)


def init_keypad_driver():
    factory = rpi_gpio.KeypadFactory()

    keypad = factory.create_keypad(keypad=KEYPAD,row_pins=ROW_PINS,col_pins=COL_PINS,key_delay=100)

    keypad.registerKeyPressHandler(handle_keypad_press)


def handle_keypad_press(key):

    global input_key_codes

    if key == '*':
        print("Clearing input .. ")

        input_key_codes = DEFAULT_INDENT

        display_to_lcd(None, None, show_input_keycode=True)

    elif key == '#':

        if len(input_key_codes.strip()) < DEFAULT_KEYCODE_LENGTH:

            display_to_lcd("Incomplete !!! ", 2,
                           show_input_keycode=False, duration=1)

            display_to_lcd(None, None, show_input_keycode=True)

            return

        print("Connecting to REST API Server .. ")
        display_to_lcd("Checking ...... ", 2, show_input_keycode=False)

        with_right = validate_keycode(input_key_codes)

        if with_right:

            display_to_lcd("Valid Keycode!", 2,
                           show_input_keycode=False, duration=1)

            input_key_codes = DEFAULT_INDENT

            open_lock()

            display_to_lcd(None, None, show_input_keycode=True)

        else:

            display_to_lcd("Invalid Keycode!", 2,
                           show_input_keycode=False, duration=1)

            input_key_codes = DEFAULT_INDENT

            display_to_lcd(None, None, show_input_keycode=True)

    else:

        if len(input_key_codes.strip()) == DEFAULT_KEYCODE_LENGTH:

            display_to_lcd("Exceed Limit !!! ", 2,
                           show_input_keycode=False, duration=1)

            display_to_lcd(None, None, show_input_keycode=True)

            return

        input_key_codes += str(key)

        print(f"input_key_codes :: {input_key_codes}")

        display_to_lcd(None, None, show_input_keycode=True, duration=0.2)


def validate_keycode(keycode):
    with_right = False
    keycode = keycode.strip()

    print(keycode)

    password = "123789"  # The password to open the elevator

    if password == keycode:
        with_right = True
        return with_right


def main():

    print("Starting our RPi Keypad Database Security System .. ")

    display_to_lcd("Initializing .. ", 1)     ##

    init_keypad_driver()

    display_to_lcd(None, None, show_input_keycode=True)
##
    print("Press buttons on your keypad. Ctrl+C to exit.")


if name == "__main__":

    try:
        
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        pass

    finally:
        cleanup()