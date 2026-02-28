import asyncio
import aioble
import bluetooth
from micropython import const
from machine import Pin, PWM, Timer
import time


class FilteredServo:
    def __init__(self, pin):
        self.servo = PWM(Pin(pin))
        self.servo.freq(50)
        self.angle = 130
        self.target_angle = 130
        self.rate = 30  # degrees per second

    def set_angle(self, angle):
        self.target_angle = angle

    def update(self, dt):
        if abs(self.target_angle - self.angle) < 0.1:
            self.angle = self.target_angle
        else:
            delta = self.target_angle - self.angle
            step = self.rate * dt
            if abs(delta) < step:
                self.angle = self.target_angle
            else:
                self.angle += step if delta > 0 else -step

        min_duty = 1638
        max_duty = 8192
        duty = int(min_duty + (self.angle/180) * (max_duty - min_duty))
        self.servo.duty_u16(duty)

servo1 = FilteredServo(21)
servo2 = FilteredServo(28)
servo3 = FilteredServo(27)
servo4 = FilteredServo(26)
servo5 = FilteredServo(19)


def set_servo_angle(servo, angle):
    #angle = 90 - angle
    min_duty = 1638
    max_duty = 8192
    duty = int(min_duty + (angle/180) * (max_duty - min_duty))
    servo.duty_u16(duty)

def conversion_function(x):
    meters = (10*x)/255

    if meters < 0.5:
        p = 1
    elif meters < 4:
        p = int((((meters-0.5)/4-0.5)-1)**2)
    else:
        p = 0

    return 120 + p*(140-120)

def apply_BLE_data(data: bytes):
    if not data or len(data) < 5:
        print("apply_BLE_data: ignoring short packet", data)
        return
    
    angle1 = conversion_function(data[0])
    angle2 = conversion_function(data[1])
    angle3 = conversion_function(data[2])
    angle4 = conversion_function(data[3])
    angle5 = conversion_function(data[4])
    
    servo1.set_angle(angle1)
    servo2.set_angle(angle2)
    servo3.set_angle(angle3)
    servo4.set_angle(angle4)
    servo5.set_angle(angle5)

_SERVICE_UUID = bluetooth.UUID("12345678-1234-5678-1234-56789abcdef0")
_CHARACTERISTIC_UUID = bluetooth.UUID("12345678-1234-5678-1234-56789abcdef1")

_ADV_INTERVAL_US = const(250000)

service = aioble.Service(_SERVICE_UUID)
characteristic = aioble.Characteristic(service, _CHARACTERISTIC_UUID, write=True, write_no_response=True, notify=True)

aioble.register_services(service)

timer = Timer(-1)
last_time = time.ticks_ms()
def timer_callback(t):
    global last_time
    current_time = time.ticks_ms()
    dt = (current_time - last_time) / 1000.0
    last_time = current_time
    
    servo1.update(dt)
    servo2.update(dt)
    servo3.update(dt)
    servo4.update(dt)
    servo5.update(dt)
timer.init(period=20, mode=Timer.PERIODIC, callback=timer_callback)

async def main():
    while True:
        print("Advertising...")
        async with await aioble.advertise(_ADV_INTERVAL_US, name="LIDARHeadband",
            services=[_SERVICE_UUID]) as conn:
            print("Connected!")
            
            try:
                while True:
                    await characteristic.written()
                    data = characteristic.read()
                    apply_BLE_data(data)

            except Exception as e:
                print("Connection lost or error:", e)

asyncio.run(main())
