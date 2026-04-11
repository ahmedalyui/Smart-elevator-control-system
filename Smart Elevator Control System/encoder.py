import RPi.GPIO as GPIO
import time

IN1 = 16
IN2 = 18
EN = 32

sp_forward = 1.743
sp_backward = 1.494

GPIO.setmode(GPIO.BOARD)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(EN, GPIO.OUT)

pwm = GPIO.PWM(EN, 10)
pwm.start(0)


def motor_forward(num_floors):
    GPIO.output(IN1, True)
    GPIO.output(IN2, False)
    pwm.ChangeDutyCycle(100)
    time.sleep(sp_forward * num_floors)
    motor_stop()


def motor_backward(num_floors):
    GPIO.output(IN1, False)
    GPIO.output(IN2, True)
    pwm.ChangeDutyCycle(100)
    time.sleep(sp_backward * num_floors)
    motor_stop()


def motor_stop():
    GPIO.output(IN1, False)
    GPIO.output(IN2, False)
    pwm.ChangeDutyCycle(0)


# Safe test section
if __name__ == "__main__":
    try:
        motor_forward(1)
        time.sleep(1)
        motor_backward(1)

    except KeyboardInterrupt:
        pass

    finally:
        motor_stop()
        GPIO.cleanup()