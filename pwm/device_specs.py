# -*- coding: utf-8 -*-

from enum import Enum

class DeviceType(Enum):
    SERVO = 1
    ESC = 2

class ESCModels(Enum):
    QuicRun_WP_16BL30 = 1
    HOBBYWING_WP_1625 = 2


class ServoModels(Enum):
    D115F = 1001
    E6001 = 1002

specs = {
    ServoModels.D115F: {
        'Frequency': 75,
        'PWM_min': 1380,
        'PWM_mid': 1538,
        'PWM_max': 1742
    },
    ServoModels.E6001: {
        'Frequency': 62,
        'PWM_min': 985, # Actual output: 994
        'PWM_mid': 1470, # Actual output: 1484
        'PWM_max': 1990  # Actual output: 2015
    },
    ESCModels.QuicRun_WP_16BL30: {
        'Frequency': 75,
        'PWM_min': 1220,
        'PWM_mid': 1520,
        'PWM_max': 1820
    },
    ESCModels.HOBBYWING_WP_1625: {
        'Frequency': 62,
        'PWM_min': 1000, # Actual output: 1012
        'PWM_mid': 1465, # Actual output: 1483
        'PWM_max': 1964  # Actual output: 1982
    }
}
