""" TODO:
"""
import enum
from configparser import ConfigParser


class ValidationMode(enum.Enum):
    """ Config validation mode """
    CLASSIC = 'classic'
    STRICT = 'strict'
    PARANOIA = 'paranoia'


class Status(enum.Enum):
    """ Validation status """
    SUCCESS = 'success'
    FAIL = 'fail'
    WARN = 'warning'
    PARANOIA = 'paranoia'

    def exit_code(self, mode: ValidationMode) -> int:
        """ Return exit code """
        if self == Status.FAIL:
            return 1
        _exit_vals = {
            ValidationMode.CLASSIC: [
                Status.SUCCESS, Status.WARN, Status.PARANOIA
            ],
            ValidationMode.STRICT: [Status.SUCCESS, Status.PARANOIA],
            ValidationMode.PARANOIA: [Status.SUCCESS]
        }
        if self in _exit_vals[mode]:
            return 0
        return 1


class App(object):

    def __init__(self, mode: ValidationMode):
        self._mode = mode

    @property
    def mode(self) -> ValidationMode:
        """ Current app's validation mode """
        return self._mode

    def run(self) -> Status:
        """ TODO """
        import random
        statuses = ['success', 'fail', 'warning', 'paranoia']
        stat = random.choice(statuses)
        return Status(stat)

    @classmethod
    def from_config(cls, cfg: ConfigParser) -> 'App':
        """ TODO """
        run_mode = ValidationMode(cfg.get('run', 'mode'))
        return App(run_mode)
