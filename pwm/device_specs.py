# -*- coding: utf-8 -*-

from enum import Enum
class device_type(Enum):
    SERVO = 1
    ESC = 2

class esc_models(Enum):
    QuicRun_WP_16BL30 = 1

class servo_models(Enum):
    D115F = 1001


specs = {
    servo_models.D115F: {
        'Frequency': 75,
        'PWM_min': 1380,
        'PWM_mid': 1538,
        'PWM_max': 1742
    },
    esc_models.QuicRun_WP_16BL30: {
        'Frequency': 75,
        'PWM_min': 1220,
        'PWM_mid': 1520,
        'PWM_max': 1820
    }
}
