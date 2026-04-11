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
from enum import Enum, auto
from circuits import Event


class AppEvent(Event):
    """AppEvent"""

    def __init__(self, event, arg0=0, arg1=0, obj=None):
        super(AppEvent, self).__init__()
        self.event = event
        self.arg0 = arg0
        self.arg1 = arg1
        self.obj = obj

    class Value(Enum):
        Null = 0
        # Timer = auto()
        System = auto()  # arg0=<SystemSrc>
        User = auto()  # arg0=<UserButton>

        def __int__(self):
            return self.value

        @classmethod
        def has_value(cls, value):
            return value in cls._value2member_map_

    class SystemSrc(Enum):
        Null = 0
        Timer1Hz = auto()
        SplashShow = auto()
        SplashDone = auto()
        StartAgent = auto()
        StopAgent = auto()
        AgentStarted = auto()
        AgentStopped = auto()
        ToolsInfo = auto()  # arg1 = number of tools loaded in string
        SkillsInfo = auto()  # arg1 = number of skills in "x/y" format
        ServicesCronInfo = auto()  # arg1 = "started"
        ServicesHeartbeatInfo = auto()  # arg1 = "started"
        ServicesGatewayInfo = auto()  # arg1 = gateway ip and port in format "ip:port"
        ChannelsInfo = auto()  # arg1 = channel in string format e.g. "telegram"
        RefreshStateInfo = auto()
        Shutdown = auto()

    # class TimerSrc(Enum):
    #     Null = 0
    #     Timer1Hz = auto()

    class UserButton(Enum):
        Null = 0
        ButtonKey = auto()
        ButtonA = auto()
        ButtonB = auto()
        ButtonStartStop = auto()
        ButtonExit = auto()
