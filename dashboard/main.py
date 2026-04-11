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
import signal
import logging
from circuits import Manager

from version import VERSION
from context import Context
from app.app import App
from agent.agent import Agent

###############################################################################
log_level = logging.DEBUG  # log_level = logging.INFO
logging.basicConfig(
    level=log_level,
    format="%(levelname)s: %(message)s",
)
# logging.basicConfig(level=log_level, format="%(asctime)-15s %(name)-8s %(levelname)s: %(message)s",)
logger = logging.getLogger(__name__)


if __name__ == "__main__":
    logger.debug(f"start dashboard version {VERSION}")
    context = Context(app=App.channel, agent=Agent.channel)

    mgr = Manager()
    mgr += App(context).register(mgr)
    mgr += Agent(context).register(mgr)

    try:
        mgr.run()
    except KeyboardInterrupt:
        logger.debug(f"KeyboardInterrupt")
    except Exception as e:
        logger.debug(f"Error: {e}")
    finally:
        mgr.stop()
        logger.debug(f"exit")
