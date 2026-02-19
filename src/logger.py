import logging
import time

import os
if not os.path.exists("logs"):
    os.mkdir("logs")

f = logging.Formatter("%(asctime)s - [%(name)s][%(levelname)s]: %(message)s", "%H:%M:%S")
_logger = logging.getLogger("Liminal Client")
_logger.setLevel(10)
sh = logging.StreamHandler()
sh.formatter = f
_logger.addHandler(sh)
file = f"./logs/{time.asctime().replace(":","-")}.log"
if not os.path.exists(file): open(file, "x", encoding="utf-8").write("")
fh = logging.FileHandler(file)
fh.formatter = f
_logger.addHandler(fh)

deb = debug = _logger.debug
inf = info = _logger.info
warn = warning = _logger.warning
err = error = _logger.error
crit = critical = _logger.critical
fat = fatal = _logger.fatal