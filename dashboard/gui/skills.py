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
import re
import logging
from enum import Enum
from unihiker import GUI

from .lcd_const import *
from common.pyprof import PyProf
from common.event import AppEvent


class SkillsWidget(PyProf):
    channel = "skills"

    WIDGET_TOP = 72
    WIDGET_HEIGHT = 32
    ICON_WIDTH, ICON_HEIGHT = 24, 24
    FONT_SIZE = 14

    PB_X, PB_Y = 100, WIDGET_TOP + 8
    PB_W, PB_H = 80, 18
    PB_COLOR = "#3B82F6"

    def __init__(self, gui: GUI):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.logger.debug(f"{self.name} init: pid={os.getpid()}")

        self.handlers = {
            AppEvent.Value.System: self.handleEventSystem,
        }
        self.switchSystem = {
            AppEvent.SystemSrc.SkillsInfo: self.handleSkillsInfo,
            AppEvent.SystemSrc.AgentStopped: self.handleAgentStopped,
        }
        self.skills = "-/-"
        # self.skills = "0/0"

        self.group = gui.draw_round_rect(
            x=0,
            y=self.WIDGET_TOP,
            w=LCD_WIDTH,
            h=self.WIDGET_HEIGHT,
            width=BORDER_WIDTH,
            r=BORDER_RADIUS,
            color="#0B13ED",
        )
        self.icon = gui.draw_image(
            x=10,
            y=self.WIDGET_TOP + 4,
            w=self.ICON_WIDTH,
            h=self.ICON_HEIGHT,
            image="./assets/skills.png",
        )
        gui.draw_text(
            x=40,
            y=self.WIDGET_TOP + 4,
            text="Skills",
            color="#788296",
            font_size=self.FONT_SIZE,
        )
        self.text = gui.draw_text(
            x=230,
            y=self.WIDGET_TOP + 4,
            text=self.skills,
            color="white",
            font_size=self.FONT_SIZE,
            anchor="ne",
        )

        self.pb_frame = gui.draw_rect(
            x=self.PB_X,
            y=self.PB_Y,
            w=self.PB_W,
            h=self.PB_H,
            color=self.PB_COLOR,
            width=2,
        )
        self.pb_progress = gui.fill_rect(
            x=self.PB_X, y=self.PB_Y, w=0, h=self.PB_H, color=self.PB_COLOR
        )  # Initial width 0

    def started(self, *args):
        self.logger.debug(f"{self.name} started: pid={os.getpid()}")

    def handleEventSystem(self, event):
        # self.logger.debug(
        #     f'{self.name}: handleEventSystem: event={event.event}, arg0={event.arg0}, arg1={event.arg1}, obj={event.obj}')
        self.switchSystem.get(event.arg0, self.unsupportedHandler)(event)

    def handleAgentStopped(self, event):
        self.logger.debug(
            f"{self.name}: handleAgentStopped: event={event.event}, arg0={event.arg0}, arg1={event.arg1}, obj={event.obj}"
        )
        self.skills = "-/-"
        self._updateBar(0, 1)
        self.text.config(text=self.skills)

    def handleSkillsInfo(self, event):
        self.logger.debug(
            f"{self.name}: handleSkillsInfo: event={event.event}, arg0={event.arg0}, arg1={event.arg1}, obj={event.obj}"
        )
        skills = event.arg1
        if skills is None and self.skills == skills:
            return

        match = re.search(r"(\d+)/(\d+)", skills)
        if match:
            numerator = match.group(1)
            denominator = match.group(2)
            self._updateBar(numerator, denominator)

            self.text.config(text=skills)
            self.skills = skills

    def _updateBar(self, numerator, denominator):
        percentage = int(int(numerator) * self.PB_W / int(denominator))
        self.logger.debug(
            f"{self.name}: handleEventSystem: numerator={numerator}, denominator={denominator}, percentage={percentage}"
        )
        self.pb_frame.config(w=self.PB_W)
        self.pb_progress.config(w=percentage)
