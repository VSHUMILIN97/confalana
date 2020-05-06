from functools import partial
from typing import Callable

import click

STYLES = {
    'err': partial(click.style, fg='red', bold=True),
    'scs': partial(click.style, fg='green', bold=True),
    'dft': partial(click.style, fg='white', bold=False),
    'wrn': partial(click.style, fg='yellow', bold=True)
}


def make_echo(
        msg: str,
        *,
        style: str = 'dft',
        blink: bool = False,
        underline: bool = False
) -> Callable[[], None]:
    """ Print message to the stdout """
    def _wrap_echo() -> None:
        """ Wrap echo, to perform it on the request """
        click.echo(STYLES[style](msg, blink=blink, underline=underline))
    return _wrap_echo
