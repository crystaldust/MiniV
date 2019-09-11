# -*- coding: utf-8 -*-

import keyboard

import grpc
import queue
import threading
import pwmio_pb2
import pwmio_pb2_grpc


class PWMIOClient(object):
    def __init__(self, addr):
        channel = grpc.insecure_channel(addr)
        self.stub = pwmio_pb2_grpc.pwmio_serviceStub(channel)

        self.steerQueue = queue.Queue(maxsize=10)
        steerThread = threading.Thread(target=self.sendSteerRPC)
        steerThread.daemon = True
        steerThread.start()

        self.throttleQueue = queue.Queue(maxsize=10)
        throttleThread = threading.Thread(target=self.sendThrottleRPC)
        throttleThread.daemon = True
        throttleThread.start()

        self.accelQueue = queue.Queue(maxsize=10)
        accelThread = threading.Thread(target=self.sendAccelRPC)
        accelThread.daemon = True
        accelThread.start()

    def setSteer(self, angle):
        self.steerQueue.put(angle)

    def setThrottle(self, throttle):
        self.throttleQueue.put(throttle)

    def setAccel(self, accel):
        self.accelQueue.put(accel)

    def generateSteerReq(self):
        while True:
            angle = self.steerQueue.get()
            req = pwmio_pb2.steer_request(angle=angle)
            yield req

    def generateThrottleReq(self):
        while True:
            throttle = self.throttleQueue.get()
            req = pwmio_pb2.throttle_request(throttle=throttle)
            yield req

    def generateAccelReq(self):
        while True:
            accel = self.accelQueue.get()
            req = pwmio_pb2.accel_request(accel=accel)
            yield req

    def sendSteerRPC(self):
        response = self.stub.Steer(self.generateSteerReq())
        for resp in response:
            print("got steer response: %s, code is %d, msg is %s" %
                  (resp.status.ok, resp.status.code, resp.status.msg))

    def sendThrottleRPC(self):
        response = self.stub.Throttle(self.generateThrottleReq())
        for resp in response:
            print("got throttle response: %s, code is %d, msg is %s" %
                  (resp.status.ok, resp.status.code, resp.status.msg))

    def sendAccelRPC(self):
        response = self.stub.Accel(self.generateAccelReq())
        for resp in response:
            print("got accel response: %s, code is %d, msg is %s" %
                  (resp.status.ok, resp.status.code, resp.status.msg))


if __name__ == "__main__":
    print('ready ...')
    car = PWMIOClient(addr='127.0.0.1:50051')
    while True:
        print("press w/s/a/d key to control, q to exit:")
        key = keyboard.readkey()
        if key == 'w':
            print('press w')
            car.setAccel(accel=1)
        elif key == 's':
            print('press s')
            car.setThrottle(throttle=1)
        elif key == 'a':
            print('press a')
            car.setSteer(angle=-1)
        elif key == 'd':
            print('press d')
            car.setSteer(angle=1)
        elif key == 'q':
            print('press q, bye')
            break
