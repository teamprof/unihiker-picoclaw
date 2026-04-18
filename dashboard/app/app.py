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
import threading
import logging
from circuits import handler, Event, Timer
from circuits.core.events import started

import config
from common.pyprof import PyProf
from common.event import AppEvent
from gui.splash import GuiSplash
from gui.home import GuiHome


class timer1HzEvent(Event):
    """timer1HzEvent"""


class App(PyProf):
    channel = "app"

    def __init__(self, ctx):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.logger.debug(f"{self.name} init: pid={os.getpid()}")

        self.context = ctx
        self.agentStarted = False
        self.refreshState = False
        self.handlers = {
            AppEvent.Value.User: self.handleEventUser,
            AppEvent.Value.System: self.handleEventSystem,
        }
        self.switchSystem = {
            AppEvent.SystemSrc.SplashShow: self.handleSplashShow,
            AppEvent.SystemSrc.SplashDone: self.handleSplashDone,
            AppEvent.SystemSrc.AgentStarted: self.handleAgentStarted,
            AppEvent.SystemSrc.AgentStopped: self.handleAgentStopped,
            AppEvent.SystemSrc.ToolsInfo: self.handleGatewayState,
            AppEvent.SystemSrc.SkillsInfo: self.handleGatewayState,
            AppEvent.SystemSrc.ChannelsInfo: self.handleGatewayState,
            AppEvent.SystemSrc.ServicesCronInfo: self.handleGatewayState,
            AppEvent.SystemSrc.ServicesHeartbeatInfo: self.handleGatewayState,
            AppEvent.SystemSrc.ServicesGatewayInfo: self.handleGatewayState,
            AppEvent.SystemSrc.McpReady: self.handleMcpReady,
            AppEvent.SystemSrc.Shutdown: self.handleShutdown,
        }
        self.switchUser = {
            AppEvent.UserButton.ButtonA: self.handleStartStop,
            AppEvent.UserButton.ButtonB: self.handleExit,
            AppEvent.UserButton.ButtonStartStop: self.handleStartStop,
            AppEvent.UserButton.ButtonExit: self.handleExit,
        }

        self.gui = GuiSplash().register(self)
        Timer(1, timer1HzEvent(), persist=True).register(self)

    def started(self, *args):
        self.logger.debug(
            f"{self.name} started: pid={os.getpid()}, thread={threading.current_thread().name}"
        )
        # self.logger.debug(f"{self.name} started: pid={os.getpid()}")
        # self.fire(started(*args), self.gui)

    def ready(self, *args):
        self.logger.debug(f"{self.name} ready: pid={os.getpid()}")

    # def timer1HzEvent(self):
    #     self.logger.debug(f"{self.name}: timerEvent: pid={os.getpid()}")
    #     # self.postEvent(AppEvent.Value.System, AppEvent.SystemSrc.Timer1Hz, dest = self.parent)

    def handleEventUser(self, event):
        # self.logger.debug(
        #     f'{self.name}: handleEventUser: event={event.event}, arg0={event.arg0}, arg1={event.arg1}, obj={event.obj}')
        self.switchUser.get(event.arg0, self.unsupportedHandler)(event)

    def handleStartStop(self, event):
        self.logger.debug(
            f"{self.name}: handleStartStop: event={event.event}, arg0={event.arg0}, arg1={event.arg1}, obj={event.obj}"
        )

        dst = self.context.agent
        cmd = (
            AppEvent.SystemSrc.StopAgent
            if self.agentStarted
            else AppEvent.SystemSrc.StartAgent
        )
        dst and self.postEvent(AppEvent.Value.System, cmd, dest=dst)

    def handleExit(self, event):
        self.logger.debug(
            f"{self.name}: handleExit: event={event.event}, arg0={event.arg0}, arg1={event.arg1}, obj={event.obj}"
        )
        dst = self.context.agent
        dst and self.postEvent(
            AppEvent.Value.System, AppEvent.SystemSrc.Shutdown, dest=dst
        )
        self.postEvent(AppEvent.Value.System, AppEvent.SystemSrc.Shutdown)

    def handleEventSystem(self, event):
        # self.logger.debug(
        #     f'{self.name}: handleEventSystem: event={event.event}, arg0={event.arg0}, arg1={event.arg1}, obj={event.obj}')
        self.switchSystem.get(event.arg0, self.unsupportedHandler)(event)

    def handleGatewayState(self, event):
        if isinstance(self.gui, GuiHome):
            self.logger.debug(
                f"{self.name}: handleGatewayState: event={event.event}, arg0={event.arg0}, arg1={event.arg1}, obj={event.obj}"
            )
            self.postEvent(
                event.event, event.arg0, event.arg1, event.obj, dest=self.gui
            )
        else:
            self.logger.debug(
                f"{self.name}: handleGatewayState: received event={event.event} during splash"
            )
            self.refreshState = True

    def handleShutdown(self, event):
        self.logger.debug(
            f"{self.name}: handleShutdown: event={event.event}, arg0={event.arg0}, arg1={event.arg1}, obj={event.obj}"
        )
        self.gui.unregister()
        self.gui = None
        self.stop()
        os._exit(0)

    def handleAgentStarted(self, event):
        self.logger.debug(
            f"{self.name}: handleAgentStarted: event={event.event}, arg0={event.arg0}, arg1={event.arg1}, obj={event.obj}"
        )
        self.agentStarted = True
        self.postEvent(event.event, event.arg0, event.arg1, event.obj, dest=self.gui)

    def handleAgentStopped(self, event):
        self.logger.debug(
            f"{self.name}: handleAgentStopped: event={event.event}, arg0={event.arg0}, arg1={event.arg1}, obj={event.obj}"
        )
        self.agentStarted = False
        self.postEvent(event.event, event.arg0, event.arg1, event.obj, dest=self.gui)

    def handleSplashShow(self, event):
        self.logger.debug(
            f"{self.name}: handleSplashShow: event={event.event}, arg0={event.arg0}, arg1={event.arg1}, obj={event.obj}"
        )

        if hasattr(config, "MCP_PORT"):
            return

        dst = self.context.agent
        dst and self.postEvent(
            AppEvent.Value.System, AppEvent.SystemSrc.StartAgent, dest=dst
        )

    def handleSplashDone(self, event):
        self.logger.debug(
            f"{self.name}: handleSplashDone: event={event.event}, arg0={event.arg0}, arg1={event.arg1}, obj={event.obj}"
        )

        self.gui.unregister()
        self.gui = GuiHome().register(self)

        status = (
            AppEvent.SystemSrc.AgentStarted
            if self.agentStarted
            else AppEvent.SystemSrc.AgentStopped
        )
        self.postEvent(AppEvent.Value.System, status, dest=self.gui)

        if self.refreshState:
            dst = self.context.agent
            self.postEvent(
                AppEvent.Value.System, AppEvent.SystemSrc.RefreshStateInfo, dest=dst
            )
            self.refreshState = False

    def handleMcpReady(self, event):
        dst = self.context.agent
        dst and self.postEvent(
            AppEvent.Value.System, AppEvent.SystemSrc.StartAgent, dest=dst
        )
