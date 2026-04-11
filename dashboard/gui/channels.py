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


class ChannelsWidget(PyProf):
    channel = "channels"

    WIDGET_TOP = 220
    WIDGET_HEIGHT = 56
    # ICON_WIDTH = 24
    # ICON_HEIGHT = 24
    FONT_SIZE = 14

    ITEM_W = 90
    ITEM_H = 20
    ITEM_R = 4
    ITEM_FONT_SIZE = 12
    ITEM_1_X = 12
    ITEM_Y = WIDGET_TOP + 28

    COLOR_FILL_ENABLE = "#0088CC"
    COLOR_FILL_DISABLE = "black"
    COLOR_FONT_ENABLE = "white"
    COLOR_FONT_DISABLE = "#788296"

    def __init__(self, gui: GUI):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.logger.debug(f"{self.name} init: pid={os.getpid()}")

        self.handlers = {
            AppEvent.Value.System: self.handleEventSystem,
        }
        self.switchSystem = {
            AppEvent.SystemSrc.ChannelsInfo: self.handleChannelsInfo,
            AppEvent.SystemSrc.AgentStopped: self.handleAgentStopped,
        }
        self.channels = ""

        self.group = gui.draw_round_rect(
            x=0,
            y=self.WIDGET_TOP,
            w=LCD_WIDTH,
            h=self.WIDGET_HEIGHT,
            width=BORDER_WIDTH,
            r=BORDER_RADIUS,
            color="#0B13ED",
        )
        gui.draw_text(
            x=10,
            y=self.WIDGET_TOP + 4,
            text="Channels",
            color="#788296",
            font_size=self.FONT_SIZE,
        )

        self.tg_rect = gui.draw_round_rect(
            x=12,
            y=self.ITEM_Y,
            w=self.ITEM_W,
            h=self.ITEM_H,
            r=self.ITEM_R,
            fill=self.COLOR_FILL_DISABLE,
        )
        self.tg_text = gui.draw_text(
            x=20,
            y=self.ITEM_Y,
            text="telegram",
            color=self.COLOR_FONT_DISABLE,
            font_size=self.ITEM_FONT_SIZE,
        )

        self.ws_rect = gui.draw_round_rect(
            x=110,
            y=self.ITEM_Y,
            w=self.ITEM_W,
            h=self.ITEM_H,
            r=self.ITEM_R,
            fill=self.COLOR_FILL_DISABLE,
        )
        self.ws_text = gui.draw_text(
            x=114,
            y=self.ITEM_Y,
            text="whatsapp",
            color=self.COLOR_FONT_DISABLE,
            font_size=self.ITEM_FONT_SIZE,
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
        channels = ""
        self._updateTelegram(f",telegram," in f",{channels},")
        self._updateWhatsapp(f",whatsapp," in f",{channels},")
        self.channels = channels

    def handleChannelsInfo(self, event):
        # self.logger.debug(
        #     f"{self.name}: handleChannelsInfo: event={event.event}, arg0={event.arg0}, arg1={event.arg1}, obj={event.obj}"
        # )
        channels = event.arg1
        if channels is None or self.channels == channels:
            return

        self._updateTelegram(f",telegram," in f",{channels},")
        self._updateWhatsapp(f",whatsapp," in f",{channels},")
        self.channels = channels

    def _updateTelegram(self, enable):
        self.tg_rect.config(
            fill=self.COLOR_FILL_ENABLE if enable else self.COLOR_FILL_DISABLE
        )
        self.tg_text.config(
            color=self.COLOR_FONT_ENABLE if enable else self.COLOR_FONT_DISABLE
        )

    def _updateWhatsapp(self, enable):
        self.ws_rect.config(
            fill=self.COLOR_FILL_ENABLE if enable else self.COLOR_FILL_DISABLE
        )
        self.ws_text.config(
            color=self.COLOR_FONT_ENABLE if enable else self.COLOR_FONT_DISABLE
        )
