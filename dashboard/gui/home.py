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
import sys
import os
import logging
from unihiker import GUI
from circuits import Component, handler, Event, Timer

from .lcd_const import *
from .header import HeaderWidget
from .tools import ToolsWidget
from .skills import SkillsWidget
from .services import ServicesWidget
from .channels import ChannelsWidget
from .sysinfo import SysInfoWidget

from common.pyprof import PyProf
from common.event import AppEvent


# class timer1HzEvent(Event):
#     """timer1HzEvent"""


class GuiHome(PyProf):
    channel = "home"

    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.logger.debug(f"{self.name} init: pid={os.getpid()}")
        self.handlers = {
            AppEvent.Value.System: self.handleEventSystem,
        }
        self.switchSystem = {
            AppEvent.SystemSrc.ToolsInfo: self.handleToolsInfo,
            AppEvent.SystemSrc.SkillsInfo: self.handleSkillsInfo,
            AppEvent.SystemSrc.ChannelsInfo: self.handleChannelsInfo,
            AppEvent.SystemSrc.ServicesCronInfo: self.handleServicesCronInfo,
            AppEvent.SystemSrc.ServicesHeartbeatInfo: self.handleServicesHeartbeatInfo,
            AppEvent.SystemSrc.ServicesGatewayInfo: self.handleServicesGatewayInfo,
            AppEvent.SystemSrc.AgentStarted: self.handleAgentStarted,
            AppEvent.SystemSrc.AgentStopped: self.handleAgentStopped,
        }

        gui = GUI()
        self.gui = gui
        gui.fill_rect(x=0, y=0, w=LCD_WIDTH, h=LCD_HEIGHT, color=(0, 0, 0))
        self.header = HeaderWidget(gui).register(self)
        self.tools = ToolsWidget(gui).register(self)
        self.skills = SkillsWidget(gui).register(self)
        self.services = ServicesWidget(gui).register(self)
        self.channels = ChannelsWidget(gui).register(self)
        self.sysinfo = SysInfoWidget(gui).register(self)

        # For testing only
        # self.postEvent(
        #     AppEvent.Value.System, AppEvent.SystemSrc.ToolsInfo, "8", dest=self.tools
        # )
        # self.postEvent(
        #     AppEvent.Value.System,
        #     AppEvent.SystemSrc.SkillsInfo,
        #     "6/7",
        #     dest=self.skills,
        # )
        # servInfo = {
        #     "cronStarted": True,
        #     "heartbeatStarted": True,
        #     "gateway": "0.0.0.0:18790",
        # }
        # self.postEvent(
        #     AppEvent.Value.System,
        #     AppEvent.SystemSrc.ServicesInfo,
        #     servInfo,
        #     dest=self.services,
        # )
        # self.postEvent(
        #     AppEvent.Value.System,
        #     AppEvent.SystemSrc.ChannelsInfo,
        #     "telegram",
        #     dest=self.channels,
        # )
        # For testing only

        gui.on_a_click(
            lambda: self.postEvent(
                AppEvent.Value.User, AppEvent.UserButton.ButtonA, dest=self.parent
            )
        )
        gui.on_b_click(
            lambda: self.postEvent(
                AppEvent.Value.User, AppEvent.UserButton.ButtonB, dest=self.parent
            )
        )

    # def timer1HzEvent(self):
    #     # self.logger.debug(f"{self.name}: timer1HzEvent: pid={os.getpid()}")
    #     self.postEvent(AppEvent.Value.System, AppEvent.SystemSrc.Timer1Hz)

    def started(self, *args):
        self.logger.debug(f"{self.name} started: pid={os.getpid()}")
        # self.fire(started(*args), self.info)

    def handleEventSystem(self, event):
        # self.logger.debug(
        #     f'{self.name}: handleEventSystem: event={event.event}, arg0={event.arg0}, arg1={event.arg1}, obj={event.obj}')
        self.switchSystem.get(event.arg0, self.unsupportedHandler)(event)

    def handleAgentStarted(self, event):
        # self.logger.debug(
        #     f'{self.name}: handleAgentStarted: event={event.event}, arg0={event.arg0}, arg1={event.arg1}, obj={event.obj}')
        self.postEvent(event.event, event.arg0, event.arg1, event.obj, dest=self.header)

    def handleAgentStopped(self, event):
        # self.logger.debug(
        #     f'{self.name}: handleAgentStopped: event={event.event}, arg0={event.arg0}, arg1={event.arg1}, obj={event.obj}')
        self.postEvent(event.event, event.arg0, event.arg1, event.obj, dest=self.header)
        self.postEvent(event.event, event.arg0, event.arg1, event.obj, dest=self.tools)
        self.postEvent(event.event, event.arg0, event.arg1, event.obj, dest=self.skills)
        self.postEvent(
            event.event, event.arg0, event.arg1, event.obj, dest=self.services
        )
        self.postEvent(
            event.event, event.arg0, event.arg1, event.obj, dest=self.channels
        )

    def handleToolsInfo(self, event):
        # self.logger.debug(
        #     f'{self.name}: handleToolsInfo: event={event.event}, arg0={event.arg0}, arg1={event.arg1}, obj={event.obj}')
        self.postEvent(event.event, event.arg0, event.arg1, event.obj, dest=self.tools)

    def handleSkillsInfo(self, event):
        # self.logger.debug(
        #     f'{self.name}: handleSkillsInfo: event={event.event}, arg0={event.arg0}, arg1={event.arg1}, obj={event.obj}')
        self.postEvent(event.event, event.arg0, event.arg1, event.obj, dest=self.skills)

    def handleChannelsInfo(self, event):
        # self.logger.debug(
        #     f'{self.name}: handleChannelsInfo: event={event.event}, arg0={event.arg0}, arg1={event.arg1}, obj={event.obj}')
        self.postEvent(
            event.event, event.arg0, event.arg1, event.obj, dest=self.channels
        )

    def handleServicesCronInfo(self, event):
        # self.logger.debug(
        #     f'{self.name}: handleChannelsInfo: event={event.event}, arg0={event.arg0}, arg1={event.arg1}, obj={event.obj}')
        self.postEvent(
            event.event, event.arg0, event.arg1, event.obj, dest=self.services
        )

    def handleServicesHeartbeatInfo(self, event):
        # self.logger.debug(
        #     f'{self.name}: handleServicesHeartbeatInfo: event={event.event}, arg0={event.arg0}, arg1={event.arg1}, obj={event.obj}')
        self.postEvent(
            event.event, event.arg0, event.arg1, event.obj, dest=self.services
        )

    def handleServicesGatewayInfo(self, event):
        # self.logger.debug(
        #     f'{self.name}: handleServicesGatewayInfo: event={event.event}, arg0={event.arg0}, arg1={event.arg1}, obj={event.obj}')
        self.postEvent(
            event.event, event.arg0, event.arg1, event.obj, dest=self.services
        )
