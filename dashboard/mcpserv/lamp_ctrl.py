# Copyright 2026 teamprof.net@gmail.com
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this
# software and associated documentation files (the "Software"), to deal in the Software
# without restriction, including without limitation the rights to use, copy, modify,
# merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
# PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
import logging
from pathlib import Path
from pinpong.board import Pin


class LampCtrl:
    STATE_MIN = 0
    STATE_MAX = 65535
    STATE_STEP = 16384

    def __init__(self, pin: Pin):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.name = Path(__file__).name
        self.logger.debug(f"{self.name} __init__: pin={pin}")

        # self.pin = Pin(Pin.P16, Pin.OUT)
        self.pin = Pin(pin, Pin.PWM)
        self.state = self.STATE_MIN
        self.pin.write_analog(self.state)

    def on(self):
        # self.pin.write_digital(1)
        self.state = self.STATE_MAX
        self.pin.write_analog(self.state)
        self.logger.debug(f"{self.name} on: state={self.state}")

    def off(self):
        # self.pin.write_digital(0)
        self.state = self.STATE_MIN
        self.pin.write_analog(self.state)
        self.logger.debug(f"{self.name} off: state={self.state}")

    def brighter(self):
        # self.pin.write_digital(0)
        self.state = (
            self.STATE_MAX
            if self.state >= (self.STATE_MAX - self.STATE_STEP)
            else self.state + self.STATE_STEP
        )
        self.pin.write_analog(self.state)
        self.logger.debug(f"{self.name} brigher: state={self.state}")

    def dimmer(self):
        # self.pin.write_digital(0)
        self.state = (
            self.STATE_MIN
            if self.state < self.STATE_STEP
            else self.state - self.STATE_STEP
        )
        self.pin.write_analog(self.state)
        self.logger.debug(f"{self.name} dimmer: state={self.state}")
