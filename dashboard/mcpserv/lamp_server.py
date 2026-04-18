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
from pathlib import Path
from pinpong.board import Board, Pin


class LampServer:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(LampServer, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if getattr(self, "_initialized", False):
            return

        self._initialized = True

        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.name = Path(__file__).name
        self.logger.debug(
            f"{self.name} init: pid={os.getpid()}, thread={threading.current_thread().name}"
        )
        Board().begin()  # Initialize the UNIHIKER

    @staticmethod
    def getInstance():
        """Static method to access the singleton without calling the constructor."""
        if LampServer._instance is None:
            # Optional: Initialize with defaults if it doesn't exist yet
            LampServer()
        return LampServer._instance

    def run(self):
        self.logger.debug(
            f"{self.name} run: pid={os.getpid()}, thread={threading.current_thread().name}"
        )

        import config
        from .lamp_ctrl import LampCtrl

        from mcp.server.fastmcp import FastMCP
        from mcp.server.transport_security import TransportSecuritySettings

        # Custom transport security settings
        mcp = FastMCP(host="127.0.0.1")  # Protection auto-enabled
        security = TransportSecuritySettings(
            enable_dns_rebinding_protection=True,
            allowed_hosts=["127.0.0.1:*"],
            allowed_origins=["http://127.0.0.1:*"],
        )

        mcp = FastMCP(
            "Lamp server",
            host="0.0.0.0",
            port=config.MCP_PORT,
            transport_security=security,
        )

        def _get_lamp(id: str):
            instance = LampServer.getInstance()
            match id.lower():
                case "red":
                    return instance.lampR
                case "yellow":
                    return instance.lampY
                case "green":
                    return instance.lampG
                case _:
                    return None

        @mcp.tool()
        def control_lamp(id: str, action: str) -> str:
            """
            lamp server
            :param id: "red" red lamp, "yellow" yellow lamp, "green" green lamp
            :param action: "on" turn on lamp, "off" turn off lamp, "brighter" turn up the lamp brightness, "dimmer" turn down the lamp brightness
            """
            lamp = _get_lamp(id)
            if lamp is None:
                return

            instance = LampServer.getInstance()
            instance.logger.debug(f"{self.name} control_lamp_red: lamp={lamp}")
            match action.lower():
                case "on":
                    instance.logger.debug(f"{__name__}: Turning on lamp: {lamp}")
                    lamp.on()
                    return "Lamp on"
                case "off":
                    instance.logger.debug(f"{__name__}: Turning off lamp: {lamp}")
                    lamp.off()
                    return "Lamp off"
                case "brighter":
                    instance.logger.debug(f"{__name__}: Turning up lamp: {lamp}")
                    lamp.brighter()
                    return "Lamp brighter"
                case "dimmer":
                    instance.logger.debug(f"{__name__}: Turning down lamp: {lamp}")
                    lamp.dimmer()
                    return "Lamp dimmer"
                case _:
                    self.logger.warning(f"{__name__}: unsupported action - {action}")
                    return "unsupported action (either 'on', 'off', 'brighter' or 'dimmer')"

        # Board().begin()  # Initialize the UNIHIKER
        self.lampR = LampCtrl(Pin.P16)  # red lamp
        self.lampY = LampCtrl(Pin.P8)  # yellow lamp
        self.lampG = LampCtrl(Pin.P9)  # green lamp

        try:
            mcp.run(transport="streamable-http")

        finally:
            self.logger.info(f"{__name__}: run: exit")
