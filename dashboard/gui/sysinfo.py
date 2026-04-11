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
import os
import logging
from enum import Enum
from unihiker import GUI
import psutil

from .lcd_const import *
from common.pyprof import PyProf
from common.event import AppEvent


class SysInfoWidget(PyProf):
    channel = "sysinfo"

    WIDGET_TOP = 280
    FONT_SIZE = 12

    ITEM_X = 4
    ITEM_1_X, ITEM_1_Y = 220, WIDGET_TOP
    ITEM_2_X, ITEM_2_Y = 220, WIDGET_TOP + 18

    def __init__(self, gui: GUI):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.logger.debug(f"{self.name} init: pid={os.getpid()}")

        self.handlers = {
            AppEvent.Value.System: self.handleEventSystem,
        }
        self.switchSystem = {
            AppEvent.SystemSrc.Timer1Hz: self.handleTimer1Hz,
        }

        gui.draw_text(
            x=self.ITEM_X,
            y=self.ITEM_1_Y,
            text="cpu usage:",
            color="#788296",
            font_size=self.FONT_SIZE,
        )
        self.cpu = gui.draw_text(
            x=self.ITEM_1_X,
            y=self.ITEM_1_Y,
            text="-.-%",
            color="white",
            font_size=self.FONT_SIZE,
            anchor="ne",
        )

        gui.draw_text(
            x=self.ITEM_X,
            y=self.ITEM_2_Y,
            text="memory usage:",
            color="#788296",
            # color="white",
            font_size=self.FONT_SIZE,
        )
        self.mem = gui.draw_text(
            x=self.ITEM_2_X,
            y=self.ITEM_2_Y,
            text="-.-%",
            color="white",
            font_size=self.FONT_SIZE,
            anchor="ne",
        )

    def started(self, *args):
        self.logger.debug(f"{self.name} started: pid={os.getpid()}")

    def timer1HzEvent(self):
        # self.logger.debug(f"{self.name}: timer1HzEvent: pid={os.getpid()}")
        self.postEvent(AppEvent.Value.System, AppEvent.SystemSrc.Timer1Hz)

    def handleEventSystem(self, event):
        # self.logger.debug(
        #     f'{self.name}: handleEventSystem: event={event.event}, arg0={event.arg0}, arg1={event.arg1}, obj={event.obj}')
        self.switchSystem.get(event.arg0, self.unsupportedHandler)(event)

    def handleTimer1Hz(self, event):
        # self.logger.debug(
        #     f"{self.name}: handleTimer1Hz: event={event.event}, arg0={event.arg0}, arg1={event.arg1}, obj={event.obj}"
        # )

        cpuUsage = psutil.cpu_percent(interval=1)
        self.cpu.config(text=f"{cpuUsage:.1f}%")

        mem = psutil.virtual_memory()
        self.mem.config(text=f"{mem.percent:.1f}%")
