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
from circuits import handler, Event, Timer

from .gateway import Gateway
from common.pyprof import PyProf
from common.event import AppEvent


class Agent(PyProf):
    channel = "agent"

    def __init__(self, ctx):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.logger.debug(f"{self.name} init: pid={os.getpid()}")

        self.context = ctx
        self.gw = None
        self.gw_state = {}

        self.handlers = {
            AppEvent.Value.System: self.handleEventSystem,
        }
        self.switchSystem = {
            AppEvent.SystemSrc.Timer1Hz: self.handleTimer1Hz,
            AppEvent.SystemSrc.StartAgent: self.handleStartAgent,
            AppEvent.SystemSrc.StopAgent: self.handleStopAgent,
            AppEvent.SystemSrc.Shutdown: self.handleShutdown,
            AppEvent.SystemSrc.RefreshStateInfo: self.handleRefreshStateInfo,
        }

    def started(self, *args):
        self.logger.debug(f"{self.name} started: pid={os.getpid()}")

    def ready(self, *args):
        self.logger.debug(f"{self.name} ready: pid={os.getpid()}")

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
        if self.gw is None:
            return

        if self.gw and not self.gw.is_alive():
            self.gw = None

            dst = self.context.app
            dst and self.postEvent(
                AppEvent.Value.System, AppEvent.SystemSrc.AgentStopped, dest=dst
            )
        elif len(self.gw_state) != len(self.gw.state):
            changes = dict(self.gw.state.items() - self.gw_state.items())
            [self._postUpdateInfo(k, v) for k, v in changes.items()]
            self.gw_state = self.gw.state.copy()

    def handleShutdown(self, event):
        self.logger.debug(
            f"{self.name}: handleShutdown: event={event.event}, arg0={event.arg0}, arg1={event.arg1}, obj={event.obj}"
        )
        self._stopGateway()
        self.stop()

    def handleStartAgent(self, event):
        self.logger.debug(
            f"{self.name}: handleStartAgent: event={event.event}, arg0={event.arg0}, arg1={event.arg1}, obj={event.obj}"
        )

        if self.gw is None:
            self.gw = Gateway()
            self.gw.start()

        dst = self.context.app
        dst and self.postEvent(
            AppEvent.Value.System, AppEvent.SystemSrc.AgentStarted, dest=dst
        )

    def handleStopAgent(self, event):
        self.logger.debug(
            f"{self.name}: handleStopAgent: event={event.event}, arg0={event.arg0}, arg1={event.arg1}, obj={event.obj}"
        )

        if self.gw is not None:
            self._stopGateway()

        dst = self.context.app
        dst and self.postEvent(
            AppEvent.Value.System, AppEvent.SystemSrc.AgentStopped, dest=dst
        )

    def _stopGateway(self):
        self.gw and self.gw.stop()
        self.gw = None
        self.gw_state = {}

    def _postUpdateInfo(self, key, values):
        # self.logger.debug(f"{self.name}: key={key}, values={values}")
        match key:
            case "tools":
                arg0 = AppEvent.SystemSrc.ToolsInfo
                arg1 = values
            case "skills":
                arg0 = AppEvent.SystemSrc.SkillsInfo
                arg1 = values
            case "cron":
                arg0 = AppEvent.SystemSrc.ServicesCronInfo
                arg1 = values
            case "heartbeat":
                arg0 = AppEvent.SystemSrc.ServicesHeartbeatInfo
                arg1 = values
            case "gateway_ip":
                arg0 = AppEvent.SystemSrc.ServicesGatewayInfo
                arg1 = values
            case "channels":
                arg0 = AppEvent.SystemSrc.ChannelsInfo
                arg1 = values
            case _:
                self.logger.debug(
                    f"{self.name}: unsupported key={key}, values={values}"
                )
                return

        dst = self.context.app
        dst and self.postEvent(AppEvent.Value.System, arg0, arg1, dest=dst)

    def handleRefreshStateInfo(self, event):
        self.logger.debug(f"{self.name}: handleRefreshStateInfo")
        [self._postUpdateInfo(k, v) for k, v in self.gw_state.items()]
