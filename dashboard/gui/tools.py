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


class ToolsWidget(PyProf):
    channel = "tools"

    WIDGET_TOP = 40
    WIDGET_HEIGHT = 32
    ICON_WIDTH = 24
    ICON_HEIGHT = 24
    FONT_SIZE = 14

    def __init__(self, gui: GUI):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.logger.debug(f"{self.name} init: pid={os.getpid()}")

        self.handlers = {
            AppEvent.Value.System: self.handleEventSystem,
        }
        self.switchSystem = {
            AppEvent.SystemSrc.ToolsInfo: self.handleToolsInfo,
            AppEvent.SystemSrc.AgentStopped: self.handleAgentStopped,
        }
        self.tools = "-"

        self.group = gui.draw_rect(
            x=0,
            y=self.WIDGET_TOP,
            w=LCD_WIDTH,
            h=self.WIDGET_HEIGHT,
            width=BORDER_WIDTH,
            color="#0B13ED",
        )
        self.icon = gui.draw_image(
            x=10,
            y=self.WIDGET_TOP + 4,
            w=self.ICON_WIDTH,
            h=self.ICON_HEIGHT,
            image="./assets/tools.png",
        )
        gui.draw_text(
            x=40,
            y=self.WIDGET_TOP + 4,
            text="Tools loaded",
            color="#788296",
            font_size=self.FONT_SIZE,
        )
        self.text = gui.draw_text(
            x=230,
            y=self.WIDGET_TOP + 4,
            text=self.tools,
            color="white",
            font_size=self.FONT_SIZE,
            anchor="ne",
        )

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
        self.tools = "-"
        self.uiUpdateText()

    def handleToolsInfo(self, event):
        # self.logger.debug(
        #     f'{self.name}: handleToolsLoaded: event={event.event}, arg0={event.arg0}, arg1={event.arg1}, obj={event.obj}')
        self.tools = event.arg1
        self.uiUpdateText()

    def uiUpdateText(self):
        self.text.config(text=self.tools)
