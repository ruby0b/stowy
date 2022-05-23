import logging
from functools import partial


class Levels:
    FATAL = logging.FATAL
    ERROR = logging.ERROR
    WARNING = logging.WARNING
    LOG_LINKS = logging.INFO + 5
    LOG_CD_OR_PLAN = logging.INFO
    LOG_EACH_STOW = logging.DEBUG + 5
    LOG_STOW_PROCESS = logging.DEBUG + 3
    LOG_IGNORE_DETAILS = logging.DEBUG


FATAL = logging.fatal
ERROR = logging.error
EXCEPTION = logging.exception
WARNING = logging.warning
LOG_LINKS = partial(logging.log, Levels.LOG_LINKS)
LOG_CD_OR_PLAN = partial(logging.log, Levels.LOG_CD_OR_PLAN)
LOG_EACH_STOW = partial(logging.log, Levels.LOG_EACH_STOW)
LOG_STOW_PROCESS = partial(logging.log, Levels.LOG_STOW_PROCESS)
LOG_IGNORE_DETAILS = partial(logging.log, Levels.LOG_IGNORE_DETAILS)
DEBUG = LOG_IGNORE_DETAILS


def setup_logging(verbosity: int):
    """
    Setup logging depending on the same
    verbosity level that is propagated to Stow
    """
    levels = [Levels.WARNING, Levels.LOG_LINKS,
              Levels.LOG_CD_OR_PLAN, Levels.LOG_EACH_STOW,
              Levels.LOG_STOW_PROCESS, Levels.LOG_IGNORE_DETAILS]
    try:
        log_level = levels[verbosity]
    except IndexError:
        log_level = levels[-1]
    logging.basicConfig(format='*StowY*: %(message)s', level=log_level)
