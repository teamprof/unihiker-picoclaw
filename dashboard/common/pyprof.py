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
import logging
from abc import ABC, abstractmethod
from circuits import Component, handler, Event
from .event import AppEvent


class PyProf(Component):

    def __init__(self):
        super().__init__()
        self.handlers = {}

        log_level = logging.DEBUG   # log_level = logging.INFO
        logging.basicConfig(
            level=log_level, format="%(levelname)s: %(message)s",)
        # logging.basicConfig(level=log_level, format="%(asctime)-15s %(name)-8s %(levelname)s: %(message)s",)
        self.logger = logging.getLogger(__name__)

    # @property
    # @abstractmethod
    # def handlers(self):
    #     pass

    # @abstractmethod

    def postEvent(self, event, arg0=0, arg1=0, obj=None, dest=None):
        self.fire(AppEvent(event, arg0, arg1, obj),
                  self if dest is None else dest)

    @handler('AppEvent')
    def onAppEvent(self, event):
        # self.logger.debug(f'{self.name}: AppEvent: event={event.event}, arg0={event.arg0}, arg1={event.arg1}, obj={event.obj}')
        # self.logger.info(f'{self.name}: AppEvent: event={event.event}, arg0={event.arg0}, arg1={event.arg1}, obj={event.obj}')
        if event.event in self.handlers:
            self.handlers[event.event](event)
        else:
            self.unsupportedHandler(event)

    def unsupportedHandler(self, event):
        self.logger.debug(
            f'{self.name}: unsupported event={event.event}, arg0={event.arg0}, arg1={event.arg1}, obj={event.obj}')
