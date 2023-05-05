
from typing import Optional


def get_device_model() -> Optional[str]:
    """
    Search /proc/device-tree/model for the device model and return its value, if found,
    otherwise None.
    """
    try:
        with open("/proc/device-tree/model", "r", encoding="utf-8") as model_file:
            return model_file.read()
    except FileNotFoundError:
        pass
    return None


def is_raspberry_pi() -> bool:
    model = get_device_model()

    if 'raspberry pi' in model.lower():
        return True

    return False


def is_orange_pi() -> bool:
    model = get_device_model()

    if 'orangepi zero2' in model.lower():
        return True

    return False


if is_raspberry_pi():
    import RPi.GPIO as GPIO
    spi_bus = 0
    spi_device = 1
    i2c_channel = 0

elif is_orange_pi():
    import OPi.GPIO as GPIO
    GPIO.setboard(GPIO.H616)
    spi_bus = 1
    spi_device = 1
    i2c_channel = 3

else:
    raise NotImplementedError("Board no compatible")