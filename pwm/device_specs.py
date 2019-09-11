# -*- coding: utf-8 -*-

from enum import Enum

class DeviceType(Enum):
    SERVO = 1
    ESC = 2

class ESCModels(Enum):
    QuicRun_WP_16BL30 = 1

class ServoModels(Enum):
    D115F = 1001

specs = {
    ServoModels.D115F: {
        'Frequency': 75,
        'PWM_min': 1380,
        'PWM_mid': 1538,
        'PWM_max': 1742
    },
    ESCModels.QuicRun_WP_16BL30: {
        'Frequency': 75,
        'PWM_min': 1220,
        'PWM_mid': 1520,
        'PWM_max': 1820
    }
}
