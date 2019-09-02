# -*- coding: utf-8 -*-

from device_specs import DeviceType, ServoModels, ESCModels
from pwm_controller import initPWMDevice, PCA9685Controller

from approxeng.input.selectbinder import ControllerResource
from os import system
import time

servo_controller = PCA9685Controller(pwm_channel=4)
esc_controller = PCA9685Controller(pwm_channel=8)
print('PCA9685 controllers inited')

servo_device = initPWMDevice(DeviceType.SERVO, ServoModels.D115F, pwm_controller=servo_controller)
esc_device = initPWMDevice(DeviceType.ESC, ESCModels.QuicRun_WP_16BL30, pwm_controller=esc_controller)


with ControllerResource() as joystick:
    print(type(joystick).__name__)
    while joystick.connected:
        time.sleep(0.02)

        system('clear')
        lt, rt = joystick['lt', 'rt'] # range: [0, 1]
        if lt > 0.1:
            esc_device.set_dutycycle(-lt)
        else:
            esc_device.set_dutycycle(rt)

        lx = joystick['lx']
        servo_device.set_dutycycle(-lx)

        joystick.check_presses()
        if joystick.presses.start:
            print('exit')
            break

# Reset PWM & release the resources
servo_device.set_dutycycle(0)
esc_device.set_dutycycle(0)

servo_device.release()
esc_device.release()
