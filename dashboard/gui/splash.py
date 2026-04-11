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
# import sys
import os
import logging
from unihiker import GUI
from circuits import handler, Event, Timer

from common.pyprof import PyProf
from common.event import AppEvent


class GuiSplash(PyProf):
    channel = "splash"
    SPLASH_DURATION = 2

    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.logger.debug(f"{self.name} init: pid={os.getpid()}")
        self.handlers = {
            AppEvent.Value.User: self.handleEventUser,
            AppEvent.Value.System: self.handleEventSystem,
        }
        self.switchSystem = {
            AppEvent.SystemSrc.AgentStarted: self.handleAgentDone,
            AppEvent.SystemSrc.AgentStopped: self.handleAgentDone,
        }
        self.switchUser = {
            AppEvent.UserButton.ButtonA: self.handleButtonA,
        }
        self.duration = self.SPLASH_DURATION

        gui = GUI()
        self.gui = gui
        self.splash = gui.draw_image(x=0, y=40, image="./assets/splash.png")

        gui.on_a_click(
            lambda: self.postEvent(AppEvent.Value.User, AppEvent.UserButton.ButtonA)
        )
        gui.on_b_click(
            lambda: self.postEvent(
                AppEvent.Value.User, AppEvent.UserButton.ButtonB, dest=self.parent
            )
        )

    def started(self, *args):
        self.logger.debug(f"{self.name} started: pid={os.getpid()}")
        self.postEvent(
            AppEvent.Value.System, AppEvent.SystemSrc.SplashShow, dest=self.parent
        )

    # def timer1HzEvent(self):
    #     # self.logger.debug(f"{self.name}: timer1HzEvent: pid={os.getpid()}")
    #     if self.duration > 0:
    #         self.duration -= 1

    #         self.duration == 0 and self.postEvent(
    #             AppEvent.Value.System, AppEvent.SystemSrc.SplashDone, dest=self.parent
    #         )

    def handleEventSystem(self, event):
        # self.logger.debug(
        #     f'{self.name}: handleEventSystem: event={event.event}, arg0={event.arg0}, arg1={event.arg1}, obj={event.obj}')
        self.switchSystem.get(event.arg0, self.unsupportedHandler)(event)

    def handleAgentDone(self, event):
        self.logger.debug(
            f"{self.name}: handleAgentStarted: event={event.event}, arg0={event.arg0}, arg1={event.arg1}, obj={event.obj}"
        )
        self.postEvent(
            AppEvent.Value.System, AppEvent.SystemSrc.SplashDone, dest=self.parent
        )

    def handleEventUser(self, event):
        # self.logger.debug(
        #     f'{self.name}: handleEventUser: event={event.event}, arg0={event.arg0}, arg1={event.arg1}, obj={event.obj}')
        self.switchUser.get(event.arg0, self.unsupportedHandler)(event)

    def handleButtonA(self, event):
        self.logger.debug(
            f"{self.name}: handleButtonA: event={event.event}, arg0={event.arg0}, arg1={event.arg1}, obj={event.obj}"
        )
        self.postEvent(
            AppEvent.Value.System,
            AppEvent.SystemSrc.SplashDone,
            dest=self.parent,
        )
