import logging
import time
from . import appdata

deb = debug = lambda msg, *args: None
inf = info = lambda msg, *args: None
warn = warning = lambda msg, *args: None
err = error = lambda msg, *args: None
crit = critical = lambda msg, *args: None
fat = fatal = lambda msg, *args: None

import os
def init():
    if not os.path.exists(appdata.get_path("logs/")):
        os.mkdir(appdata.get_path("logs/"))

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

    global deb, debug
    global inf, info
    global warn, warning
    global err, error
    global crit, critical
    global fat, fatal

    deb = debug = _logger.debug
    inf = info = _logger.info
    warn = warning = _logger.warning
    err = error = _logger.error
    crit = critical = _logger.critical
    fat = fatal = _logger.fatal