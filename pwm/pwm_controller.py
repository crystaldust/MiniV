# -*- coding: utf-8 -*-
from adafruit_pca9685 import PCA9685
import board
import busio

from device_specs import specs


"""
PCA9685Controller, implements the interfaces:
    - set_frequency
    - set_dutycycle

    as a 'PWMController'
"""
class PCA9685Controller:
    def __init__(self, i2c_bus_no=1, pwm_channel=0):
        if i2c_bus_no == 0:
            i2c_bus = busio.I2C(board.SCL_1, board.SDA_1)
        elif i2c_bus_no == 1:
            i2c_bus = busio.I2C(board.SCL, board.SDA)
        else:
            raise RuntimeError('Invalid I2C bus number {}, either 0 or 1'.format(i2c_bus))

        try:
            self.pca = PCA9685(i2c_bus)
            self.pwm_channel = pwm_channel
        except Exception as e:
            print('Failed to init PCA9685 module, error: {}\nMake sure it is plugined correctly to the device'.format(e))
            exit(1)

    """
    freq: Set the frequency of PCA9685 module. Not that the value would change a little
    after pca.frequency is set. That is pca.frequency is not exactly the same with freq
    when coding.
    """
    def set_frequency(self, freq):
        self.pca.frequency = freq
    
    """
    pwm_channel: int, range [0, 15], PCA9685 has 16 PWM channels
    dc: float, range [0, 1], PCA9685 has 16 PWM channels

    """
    def set_dutycycle(self, dc):
        # Convert dc value to PCA9685 value, PCA9685 uses 16bit data,
        # just multiply 2^16, which is 65536
        pca9685_value = int(dc * 65536)
        print('dc:', dc, 'pca_dc:', pca9685_value)
        self.pca.channels[self.pwm_channel].duty_cycle = pca9685_value

    def release(self):
        self.pca.deinit()


class PWMDevice:
    def __init__(self, device_type, device_model, pwm_controller):
        print('create PWMDevice', device_type, device_model)
        self.device_type = device_type # TODO device_type not used for now
        self.device_model = device_model

        device_spec = specs[device_model]

        self.pwm_controller = pwm_controller
        # Tips here: don't set self.pca.frequency and refer it, the freq would change a little bit from pca
        frequency = device_spec['Frequency']
        self.period = 1000000 / frequency

        print("freq:", frequency, "period:", self.period)

        self.dc_min = device_spec['PWM_min'] / self.period
        self.dc_mid = device_spec['PWM_mid'] / self.period
        self.dc_max = device_spec['PWM_max'] / self.period
        self.dc_gaps = [self.dc_mid - self.dc_min, self.dc_max - self.dc_mid]

        self.pwm_controller.set_frequency(frequency)

    def release(self):
        self.pwm_controller.release()


    def set_dutycycle(self, dc):
        # Map dc [-1, 1] to the real duty cycle
        # TODO: Maybe there should be more mapping rules, like non-linear maps?
        if dc >=0:
            dc_value = self.dc_mid + dc * self.dc_gaps[1]
        else:
            dc_value = self.dc_mid + dc * self.dc_gaps[0]


        self.pwm_controller.set_dutycycle(dc_value)

# TODO Make the param pca an abstract "PWM controller", allow more modules to 
# send PWM signal

def initPWMDevice(device_type, device_model, pwm_controller):
    return PWMDevice(device_type, device_model, pwm_controller)
