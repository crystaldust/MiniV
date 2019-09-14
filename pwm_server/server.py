# -*- coding: utf-8 -*-

import os
import sys

parent_path = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, parent_path+'/pwm')

from device_specs import DeviceType, ESCModels, ServoModels
from pwm_controller import PCA9685Controller, PWMDevice, initPWMDevice

import pwmio_pb2
import pwmio_pb2_grpc
from concurrent import futures
import math
import time
import grpc


class Car(pwmio_pb2_grpc.pwmio_serviceServicer):
    def __init__(self, init_steer, steer_model, steer_channel, revers_steer, init_servo, servo_model, servo_channel, revers_servo):
        if init_steer:
            # 设置舵机是否反转及初始化舵机
            self.init_steer(steer_model, steer_channel, revers_steer)
        if init_servo:
            # 设置电调是否反转及初始化电调
            self.init_servo(servo_model, servo_channel, revers_servo)

    def init_steer(self, steer_model, steer_channel, revers_steer):
            self.revers_steer = revers_steer
            steer_controller = PCA9685Controller(pwm_channel=steer_channel)
            self.steer = initPWMDevice(
                DeviceType.ESC, steer_model, pwm_controller=steer_controller)

    def init_servo(self, servo_model, servo_channel, revers_servo):
            self.revers_servo = revers_servo
            servo_controller = PCA9685Controller(pwm_channel=servo_channel)
            self.servo = initPWMDevice(
                DeviceType.SERVO, servo_model, pwm_controller=servo_controller)

    def InitSteer(self, request, context):
        if request.steer_type in ESCModels.__members__:
            self.init_steer(request.steer_model, request.steer_channel, request.revers_steer)
            return pwmio_pb2.init_steer_reply(status=pwmio_pb2.pwm_status(ok=True))
        else:
            return pwmio_pb2.init_steer_reply(status=pwmio_pb2.pwm_status(ok=False, code=400, msg=("bad steer type")))

    def InitServo(self, request, context):
        if request.servo_type in ESCModels.__members__:   
            self.init_servo(request.servo_model, request.servo_channel, request.revers_servo)
            return pwmio_pb2.init_servo_reply(status=pwmio_pb2.pwm_status(ok=True))
        else:
            return pwmio_pb2.init_servo_reply(status=pwmio_pb2.pwm_status(ok=False, code=400, msg=("bad steer type")))

    def Steer(self, request_iterator, context):
        """转角角度,取值 `[-PI/2, +PI/2]`
        """
        for angle in request_iterator:
            i = angle.angle
            print('got steer request:', i)
            if i < -1 * math.pi / 2 or i > math.pi / 2:
                yield pwmio_pb2.steer_reply(status=pwmio_pb2.pwm_status(ok=False, code=400, msg=("bad angle value: %s" % i)))
            dc = math.pi / 2 * i
            if self.revers_steer:
                dc = -1 * dc
            self.steer.set_dutycycle(dc=dc)
            yield pwmio_pb2.steer_reply(status=pwmio_pb2.pwm_status(ok=True))

    def Throttle(self, request_iterator, context):
        """刹车, 参数为刹车抱死产生的反向加速度, 取值范围暂定[0, 1], 待小车测定后给出最大值
        """
        for throttle in request_iterator:
            i = throttle.throttle
            print('got throttle request:', i)
            if i < 0 or i > 1:
                yield pwmio_pb2.throttle_reply(status=pwmio_pb2.pwm_status(ok=False, code=400, msg=("bad throttle value: %s" % i)))
            dc = -1 * i
            if self.revers_servo:
                dc = -1 * dc
            self.servo.set_dutycycle(dc=dc)
            yield pwmio_pb2.throttle_reply(status=pwmio_pb2.pwm_status(ok=True))

    def Accel(self, request_iterator, context):
        """加速, 参数为加速度, 取值范围[-1, 1], 负值为控制小车向与当前车头方向相反方向运动, 待小车测定后给出最大最小值范围
        """
        for accel in request_iterator:
            i = accel.accel
            print('got accel request:', i)
            if i < 0 or i > 1:
                yield pwmio_pb2.accel_reply(status=pwmio_pb2.pwm_status(ok=False, code=400, msg=("bad accel value: %s" % i)))
            dc = i
            if self.revers_servo:
                dc = -1 * dc
            self.servo.set_dutycycle(dc=dc)
            yield pwmio_pb2.accel_reply(status=pwmio_pb2.pwm_status(ok=True))


def serve(addr, car):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pwmio_pb2_grpc.add_pwmio_serviceServicer_to_server(car, server)
    server.add_insecure_port(addr)
    server.start()
    try:
        while True:
            time.sleep(60*60*24)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == "__main__":
    print('start...')
    car = Car(True, ServoModels.D115F, 4, False,
              True, ESCModels.QuicRun_WP_16BL30, 7, False)
    print('ready to server...')
    serve('[::]:50051', car)
