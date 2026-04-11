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
import subprocess
import threading
import sys
import os
import signal
import logging
import re
from config import PATH_PICOCLAW


class Gateway(threading.Thread):
    STR_STATUS = "Agent Status"
    PATTERNS = {
        "tools": r"Tools: (\d+)",
        "skills": r"Skills: ([\d/]+)",
        "cron": r"Cron service (\w+)",
        "heartbeat": r"Heartbeat service (\w+)",
        "channels": r"Channels enabled: \[(.*?)\]",
        "gateway_ip": r"Gateway started on ([\d\.]+:\d+)",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(target=self._run, *args, **kwargs)
        self.logger = logging.getLogger(__name__)
        self.proc = None
        self.state = {}
        self.return_code = None

    def is_alive(self):
        return self.return_code is None

    def stop(self):
        self.proc and os.kill(self.proc.pid, signal.SIGINT)

    def _run(self):
        self.proc = subprocess.Popen(
            [PATH_PICOCLAW, "gateway"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
        )

        # This loop blocks until the next line is available
        statusFound = False
        for line in self.proc.stdout:
            text = line.strip()
            # self.logger.debug(f"{text}")

            if statusFound:
                self.logger.debug(f"{text}")
                for key, pattern in self.PATTERNS.items():
                    match = re.search(pattern, text)
                    if match:
                        self.state[key] = match.group(1)
                        # self.logger.debug(f"self.state[{key}] = {self.state[key]}")
            else:
                statusFound = self.STR_STATUS in text

            # Optional: Force terminal refresh if you're not seeing output immediately
            sys.stdout.flush()

        self.logger.debug(f"self.state = {self.state}")
        self.return_code = self.proc.wait()
        self.logger.debug(f"Process finished with code: {self.return_code}")

        self.proc = None
