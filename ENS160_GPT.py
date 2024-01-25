import time

import pigpio


class ENS160:
    """
    Lightweight class for communicating with an ENS160 air quality sensor via I2C using pigpio.
    Follows the specifications defined in the official ENS160 data sheet: https://www.sciosense.com/products/environmental-sensors/ens160-di>
    Newer version of ENS160 data sheet: https://www.sciosense.com/wp-content/uploads/documents/SC-001224-DS-9-ENS160-Datasheet.pdf
    """

    def __init__(self, i2c_bus: int = 1, address: int = 0x53):
        """
        Creates a new instance of the ENS160 class
        :param pi: pigpio.pi instance
        :param i2c_bus: I2C bus number
        :param address: The I2C address of the ENS160 slave device
        """
        self.pi = pigpio.pi()
        self.address = address
        self.i2c = self.pi.i2c_open(i2c_bus, address)

    @property
    def operating_mode(self) -> int:
        """
        Reads the operating mode that the ENS160 is currently in.
        0 = Deep Sleep Mode (low power standby)
        1 = Idle mode (low-power)
        2 = Standard Gas Sensing Mode
        """
        return self.pi.i2c_read_byte_data(self.i2c, 0x10)

    @operating_mode.setter
    def operating_mode(self, value):
        """
        Sets the ENS160's operating mode.
        0 = Deep Sleep Mode (low power standby)
        1 = Idle mode (low-power)
        2 = Standard Gas Sensing Mode
        """
        return self.pi.i2c_read_byte_data(self.i2c, 0x10)

    @operating_mode.setter
    def operating_mode(self, value):
        """
        Sets the ENS160's operating mode.
        0 = Deep Sleep Mode (low power standby)
        1 = Idle mode (low-power)
        2 = Standard Gas Sensing Mode
        """
        if value not in [0, 1, 2, 0xF0]:
            raise Exception("Operating value you're setting must be 0, 1, or 2")
        self.pi.i2c_write_byte_data(self.i2c, 0x10, value)

    @property
    def CO2(self) -> int:
        """Reads the calculated equivalent CO2-concentration in PPM, based on the detected VOCs and hydrogen"""
        bs = self.pi.i2c_read_i2c_block_data(self.i2c, 0x24, 2)
        return self._translate_pair(bs[1], bs[0])

    @property
    def TVOC(self) -> int:
        """Reads the calculated Total Volatile Organic Compounds (TVOC) concentration in ppb"""
        bs = self.pi.i2c_read_i2c_block_data(self.i2c, 0x22, 2)
        return self._translate_pair(bs[1], bs[0])

    @property
    def AQI(self) -> int:
        """
        Reads the calculated Air Quality Index (AQI) according to the UBA
        1 = Excellent
        2 = Good
        3 = Moderate
        4 = Poor
        5 = Unhealthy
        """
        return self.pi.i2c_read_byte_data(self.i2c, 0x21)

    def reset(self) -> None:
        """Resets and returns to standard operating mode (2)"""

        self.operating_mode = 0xF0  # reset
        time.sleep(1.0)
        self.operating_mode = 1
        time.sleep(0.25)
        self.pi.i2c_write_byte_data(self.i2c, 0x12, 0x00)
        time.sleep(0.15)
        self.pi.i2c_write_byte_data(self.i2c, 0x12, 0xCC)  # reset command register
        time.sleep(0.35)
        self.operating_mode = 2
        time.sleep(0.50)

    def _translate_pair(self, high: int, low: int) -> int:
        """Converts a byte pair to a usable value."""
        value = (high << 8) + low

        if value >= 0x8000:
            return -((65535 - value) + 1)
        else:
            return value
