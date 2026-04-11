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

from .lcd_const import *
from common.pyprof import PyProf
from common.event import AppEvent


class HeaderWidget(PyProf):
    channel = "header"

    WIDGET_TOP = 0
    WIDGET_HEIGHT = 40
    ICON_W, ICON_H = 24, 24
    FONT_SIZE = 14

    TEXT_X, TEXT_Y = 32, WIDGET_TOP + 8
    ICON_STATE_X = 6
    ICON_1_X = 175
    ICON_2_X = 210
    ICON_Y = 8

    def __init__(self, gui: GUI):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.logger.debug(f"{self.name} init: pid={os.getpid()}")

        self.handlers = {
            AppEvent.Value.System: self.handleEventSystem,
        }
        self.switchSystem = {
            AppEvent.SystemSrc.AgentStarted: self.handleAgentStarted,
            AppEvent.SystemSrc.AgentStopped: self.handleAgentStopped,
        }

        self.isAgentStarted = False

        self.group = gui.draw_rect(
            x=self.WIDGET_TOP,
            y=self.WIDGET_TOP,
            w=LCD_WIDTH,
            h=self.WIDGET_HEIGHT,
            color=self._uiColor(),
            fill=self._uiColor(),
        )
        gui.draw_text(
            x=self.TEXT_X,
            y=self.TEXT_Y,
            text="PicoClaw",
            anchor="nw",
            color="white",
            font_size=self.FONT_SIZE,
        )
        self.iconState = gui.draw_image(
            x=self.ICON_STATE_X,
            y=self.ICON_Y,
            w=self.ICON_W,
            h=self.ICON_H,
            image=self._getIcon(self.isAgentStarted),
        )

        self.iconStartStop = gui.draw_image(
            x=self.ICON_1_X,
            y=self.ICON_Y,
            w=self.ICON_W,
            h=self.ICON_H,
            image=self._getIconStartStop(),
            onclick=self._uiClickStartStop,
        )
        self.iconExit = gui.draw_image(
            x=self.ICON_2_X,
            y=self.ICON_Y,
            w=self.ICON_W,
            h=self.ICON_H,
            image=self._getIconExit(),
            onclick=self._uiClickExit,
        )

    def started(self, *args):
        self.logger.debug(f"{self.name} started: pid={os.getpid()}")

    def ready(self, *args):
        self.logger.debug(f"{self.name} ready: pid={os.getpid()}, args={args}")

    def handleEventSystem(self, event):
        # self.logger.debug(
        #     f"{self.name}: handleEventSystem: event={event.event}, arg0={event.arg0}, arg1={event.arg1}, obj={event.obj}"
        # )
        self.switchSystem.get(event.arg0, self.unsupportedHandler)(event)

    def handleAgentStarted(self, event):
        self.logger.debug(
            f"{self.name}: handleAgentStarted: event={event.event}, arg0={event.arg0}, arg1={event.arg1}, obj={event.obj}"
        )
        self.isAgentStarted = True
        self._uiUpdate()

    def handleAgentStopped(self, event):
        self.logger.debug(
            f"{self.name}: handleAgentStopped: event={event.event}, arg0={event.arg0}, arg1={event.arg1}, obj={event.obj}"
        )
        self.isAgentStarted = False
        self._uiUpdate()

    def _uiClickStartStop(self):
        self.logger.debug(f"{self.name}: uiClickStartStop()")
        self.postEvent(
            AppEvent.Value.System, AppEvent.UserButton.ButtonStartStop, dest=self.parent
        )

    def _uiClickExit(self):
        self.logger.debug(f"{self.name}: uiClickExit()")
        self.postEvent(
            AppEvent.Value.System, AppEvent.UserButton.ButtonExit, dest=self.parent
        )

    def _getIconStartStop(self):
        return "./assets/stop.png" if self.isAgentStarted else "./assets/start.png"

    def _getIconExit(self):
        return "./assets/exit.png"

    def _uiUpdate(self):
        self.group.config(
            fill=self._uiColor(),
            color=self._uiColor(),
        )
        self.iconState.config(image=self._getIcon(self.isAgentStarted))
        self.iconStartStop.config(image=self._getIconStartStop())

    def _uiColor(self):
        return "#0B13ED" if self.isAgentStarted else "#788296"
        # return 'blue' if self.isAgentStarted else 'grey'

    def _getIcon(self, enable):
        return "./assets/tick.png" if enable else "./assets/cross.png"
