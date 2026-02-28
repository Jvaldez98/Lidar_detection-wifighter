from machine import Pin, PWM
import time

servo1 = PWM(Pin(0))
servo1.freq(50)

def set_servo_angle(servo, angle):
    min_duty = 1638
    max_duty = 8192
    duty = int(min_duty + (angle/180) * (max_duty - min_duty))
    servo.duty_u16(duty)

while True:
    set_servo_angle(servo1, 50)
    time.sleep(1)

    set_servo_angle(servo1, 70)
    time.sleep(1)
    