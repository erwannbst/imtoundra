"""The MIT License (MIT)
Copyright © 2022 
Maciej Sliwinski https://github.com/any-sliv/aht21_python_pigpio

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the “Software”), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE."""

import time

import pigpio

AHT_I2C_ADDR = 0x38  # Default I2C address
AHT_STATUS_BUSY = 0x01  # Status bit for busy
AHT_STATUS_CALIBRATED = 0x10  # status bit for calibrated
AHT_CMD_INIT = 0xBE  # command for initialization
AHT_CMD_TRIGGER = 0xAC  # command for trigger measurement
AHT_CMD_RESET = 0xBA  # command for soft reset
AHT_CRC_POLYNOMIAL = 0x31  # Polynomial representation
AHT_CRC_MSB = 0x80  # Most significant bit
AHT_CRC_INIT = 0xFF  # Initial value of CRC


class AHT21:
    def __init__(self, i2cNumber, crc=False):
        self.pi = pigpio.pi()
        self.handle = self.pi.i2c_open(i2cNumber, AHT_I2C_ADDR)
        self.active_crc = crc
        self._buf = bytearray(6 + crc)  # Request the CRC byte only if necessary
        assert self.handle

        while not self.is_calibrated:
            self._calibrate()

    def _write(self, data):
        self.pi.i2c_write_device(self.handle, bytearray(data))

    def _read(self, reg, len):
        (count, data) = self.pi.i2c_read_i2c_block_data(self.handle, reg, len)
        if count <= 0:
            raise Exception("Failed to read register")
        return data

    @property
    def is_ready(self):
        """The sensor is busy until the measurement is complete."""
        if bool(self._status() & AHT_STATUS_BUSY):
            return False
        return self._measure()

    @property
    def is_calibrated(self):
        """The activation of the calibration must be done before any
        measurement. If not, do a soft reset."""
        return bool(self._status() & AHT_STATUS_CALIBRATED)

    def _status(self):
        """The status byte initially returned from the sensor.
        Bit     Definition  Description
        [0:2]   Remained    Remained
        [3]     CAL Enable  0:Uncalibrated,1:Calibrated
        [4]     Remained    Remained
        [5:6]   Remained    Remained
        [7]     Busy        0:Free in dormant state, 1:Busy in measurement"""
        data = self._read(AHT_I2C_ADDR, 1)
        self._buf[0] = data[0]

        if not self.active_crc or (self._crc8() == self._buf[6]):
            return self._buf[0]
        return AHT_STATUS_BUSY  # Return the status busy and uncalibrated

    def _calibrate(self):
        self._buf[0] = AHT_CMD_INIT
        self._buf[1] = 0x08
        self._buf[2] = 0x00
        self._write(self._buf[:3])
        time.sleep(0.01)

    def _crc8(self):
        """Internal function to calcule the CRC-8-Dallas/Maxim of current
        message. The initial value of CRC is 0xFF, and the CRC8 check
        polynomial is: CRC [7:0] = 1+X^4 +X^5 +X^8"""
        crc = bytearray(1)
        crc[0] = AHT_CRC_INIT
        for byte in self._buf[:6]:
            crc[0] ^= byte
            for _ in range(8):
                if crc[0] & AHT_CRC_MSB:
                    crc[0] = (crc[0] << 1) ^ AHT_CRC_POLYNOMIAL
                else:
                    crc[0] = crc[0] << 1

        return crc[0]

    def _measure(self):
        """Internal function for triggering the AHT to read temp/humidity"""
        self._buf[0] = AHT_CMD_TRIGGER
        self._buf[1] = 0x33
        self._buf[2] = 0x00
        self._write(self._buf[:3])  # i2c.writeto(self.address, self._buf[:3])
        time.sleep(0.08)  # Wait 80ms for the measurement to be completed.
        # self.i2c.readfrom_into(self.address, self._buf)
        data = self._read(AHT_I2C_ADDR, 6)
        self._buf[0] = data[0]
        self._buf[1] = data[1]
        self._buf[2] = data[2]
        self._buf[3] = data[3]
        self._buf[4] = data[4]
        self._buf[5] = data[5]

        if not self.active_crc or (self._crc8() == self._buf[6]):
            hum = self._buf[1] << 12 | self._buf[2] << 4 | self._buf[3] >> 4
            self.humidity = hum * 100 / 0x100000
            temp = (self._buf[3] & 0xF) << 16 | self._buf[4] << 8 | self._buf[5]
            self.temperature = temp * 200.0 / 0x100000 - 50
            return True
        return False

    # def Read(self):
    #     """Returns tuple (temp, humidity). Blocking delay at readout. """
    #     read_cmd = [0xac, 0x33, 0x00]
    #     self._write(read_cmd)
    #     #todo delay perf counter?? need 80ms
    #     time.sleep(0.1)

    #     res = self._read(AHT_I2C_ADDR, 6)

    #     calc_hum = ((res[1] << 16) | (res[2] << 8) | res[3]) >> 4;
    #     calc_temp = ((res[3] & 0x0F) << 16) | (res[4] << 8) | res[5];

    #     print(f'rh: ${calc_hum}')
    #     print(f'temp: ${calc_temp}')

    #     rh = calc_hum * 100 / 1048576;
    #     temp = calc_temp * 200 / 1048576 - 50;

    #     return (temp, rh)
