import logging
import time

from . import colour as c


class Formatter(logging.Formatter):
    def __init__(self, fmt, timefmt, fmtc):
        super().__init__(fmt, timefmt, fmtc)

    def format(self, record) -> str:
        record.level = {
            'DEBUG':    c.debug,
            'INFO':     c.ok,
            'WARNING':  c.warn,
            'ERROR':    c.err,
            'CRITICAL': c.critical,
        }[record.levelname](record.levelname[:3])

        return super().format(record)

    def formatTime(self, record, format) -> str:
        ct = self.converter(record.created)
        return f"{time.strftime(format, ct)}.{int(record.msecs):03d}"


def setup_log(name, *, output=None, fmt='[{asctime} {level}] {message}', timefmt='%Y-%m-%d %H:%M:%S'):
    formatter = Formatter(fmt=fmt, timefmt=timefmt, fmtc='{')

    if isinstance(output, str):
        handler = logging.FileHandler(output)
    else:
        handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)
    log.addHandler(handler)

    return log
