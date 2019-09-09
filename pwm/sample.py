# -*- coding: utf-8 -*-

from device_specs import device_type, servo_models, esc_models
from pwm_controller import initPWMDevice, PCA9685Controller
import time

servo_controller = PCA9685Controller(pwm_channel=4)
print('PCA9685 controllers inited')
servo_device = initPWMDevice(device_type.SERVO, servo_models.D115F, pwm_controller=servo_controller)



dc = 0
while dc <= 1:
    time.sleep(0.5)
    print(dc)
    servo_device.set_dutycycle(dc)
    dc += 0.1

# Reset PWM & release the resources
servo_device.set_dutycycle(0)
servo_device.release()
