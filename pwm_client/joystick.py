# -*- coding: utf-8 -*-

import grpc
import queue
import threading
import pwmio_pb2
import pwmio_pb2_grpc
import time
from os import system

from client import PWMIOClient
from approxeng.input.selectbinder import ControllerResource


if __name__ == "__main__":
    print('ready ...')
    car = PWMIOClient(addr='127.0.0.1:50051')

    with ControllerResource() as joystick:

        while joystick.connected:
            time.sleep(0.05)
            lt, rt = joystick['lt', 'rt'] # range: [0, 1]
            if lt > 0:
                #esc_device.set_dutycycle(-lt)
                car.setThrottle(throttle=lt)
            else:
                #esc_device.set_dutycycle(rt)
                car.setAccel(accel=rt)

            lx = joystick['lx']
            car.setSteer(angle=-lx)

            joystick.check_presses()
            if joystick.presses.start:
                print('exit')
                break
