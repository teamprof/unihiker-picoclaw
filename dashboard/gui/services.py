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


class ServicesWidget(PyProf):
    channel = "services"

    WIDGET_TOP = 104
    WIDGET_HEIGHT = 116
    ICON_WIDTH = 24
    ICON_HEIGHT = 24
    FONT_SIZE = 14

    ICON_X = 12
    ITEM_X = 38
    ITEM_H = 22
    ITEM_1_Y = WIDGET_TOP + 4 + ITEM_H
    ITEM_2_Y = WIDGET_TOP + 4 + ITEM_H * 2
    ITEM_3_Y = WIDGET_TOP + 4 + ITEM_H * 3

    def __init__(self, gui: GUI):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.logger.debug(f"{self.name} init: pid={os.getpid()}")

        self.handlers = {
            AppEvent.Value.System: self.handleEventSystem,
        }
        self.switchSystem = {
            AppEvent.SystemSrc.ServicesCronInfo: self.handleServicesCronInfo,
            AppEvent.SystemSrc.ServicesHeartbeatInfo: self.handleServicesHeartbeatInfo,
            AppEvent.SystemSrc.ServicesGatewayInfo: self.handleServicesGatewayInfo,
            AppEvent.SystemSrc.AgentStopped: self.handleAgentStopped,
        }
        self.cronStarted = False
        self.heartbeatStarted = False
        self.gateway = None

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
            text="Services",
            color="#788296",
            font_size=self.FONT_SIZE,
        )
        self.iconCron = gui.draw_image(
            x=self.ICON_X,
            y=self.ITEM_1_Y,
            w=self.ICON_WIDTH,
            h=self.ICON_HEIGHT,
            image=self._getIcon(self.cronStarted),
        )
        gui.draw_text(
            x=self.ITEM_X,
            y=self.ITEM_1_Y,
            text="Cron Service",
            color="#788296",
            font_size=self.FONT_SIZE,
        )
        self.iconHeartbeat = gui.draw_image(
            x=self.ICON_X,
            y=self.ITEM_2_Y,
            w=self.ICON_WIDTH,
            h=self.ICON_HEIGHT,
            image=self._getIcon(self.heartbeatStarted),
        )
        gui.draw_text(
            x=self.ITEM_X,
            y=self.ITEM_2_Y,
            text="Heartbeat",
            color="#788296",
            font_size=self.FONT_SIZE,
        )
        self.iconGateway = gui.draw_image(
            x=self.ICON_X,
            y=self.ITEM_3_Y,
            w=self.ICON_WIDTH,
            h=self.ICON_HEIGHT,
            image=self._getIcon(self.gateway is not None),
        )
        gui.draw_text(
            x=self.ITEM_X,
            y=self.ITEM_3_Y,
            text="Gateway",
            color="#788296",
            font_size=self.FONT_SIZE,
        )
        self.gw_text = gui.draw_text(
            x=self.ITEM_X + 6,
            y=self.ITEM_3_Y + 20,
            text=self._getGatewayText(),
            color="white",
            font_size=12,
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
        started = False
        self.cronStarted = started
        self.heartbeatStarted = started
        self.gateway = None
        self.iconCron.config(image=self._getIcon(started))
        self.iconHeartbeat.config(image=self._getIcon(started))
        self.iconGateway.config(image=self._getIcon(self.gateway is not None))
        self.gw_text.config(text=self._getGatewayText())

    def handleServicesCronInfo(self, event):
        self.logger.debug(
            f"{self.name}: handleServicesCronInfo: event={event.event}, arg0={event.arg0}, arg1={event.arg1}, obj={event.obj}"
        )
        started = event.arg1 == "started"
        if self.cronStarted == started:
            return

        self.cronStarted = started
        self.iconCron.config(image=self._getIcon(started))
        self.iconGateway.config(image=self._getIcon(self.gateway is not None))
        self.gw_text.config(text=self._getGatewayText())

    def handleServicesHeartbeatInfo(self, event):
        self.logger.debug(
            f"{self.name}: handleServicesHeartbeatInfo: event={event.event}, arg0={event.arg0}, arg1={event.arg1}, obj={event.obj}"
        )
        started = event.arg1 == "started"
        if self.heartbeatStarted == started:
            return

        self.heartbeatStarted = started
        self.iconHeartbeat.config(image=self._getIcon(started))

    def handleServicesGatewayInfo(self, event):
        self.logger.debug(
            f"{self.name}: handleServicesGatewayInfo: event={event.event}, arg0={event.arg0}, arg1={event.arg1}, obj={event.obj}"
        )
        ip = event.arg1
        if self.gateway == ip:
            return

        self.gateway = ip
        self.iconGateway.config(image=self._getIcon(self.gateway is not None))
        self.gw_text.config(text=self._getGatewayText())

    def _getIcon(self, enable):
        return "./assets/tick.png" if enable else "./assets/cross.png"

    def _getGatewayText(self):
        return self.gateway if self.gateway is not None else ""
