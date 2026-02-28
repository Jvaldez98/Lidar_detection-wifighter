from machine import Pin, PWM
import time

servo1 = PWM(Pin(21))
servo2 = PWM(Pin(28))
servo3 = PWM(Pin(27))
servo4 = PWM(Pin(26))
servo5 = PWM(Pin(19))

servos = [servo1, servo2, servo3, servo4, servo5]

def set_servo_angle(servo, angle):
    min_duty = 1638
    max_duty = 8192
    duty = int(min_duty + (angle/180) * (max_duty - min_duty))
    servo.duty_u16(duty)

for servo in servos:
    servo.freq(50)
    set_servo_angle(servo, 120)
