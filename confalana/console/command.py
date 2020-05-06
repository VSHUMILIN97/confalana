""" Config schema observer """

from pathlib import Path
from typing import Optional

from click import command, option, Path as _PathType

from confalana.console.setup import load_config
from confalana.console.messaging import make_echo
from confalana.core import App


@command()
@option(
    '--config-file',
    '-c',
    type=_PathType(exists=True),
    help=(
        'Path to "confalana" settings. Will be ignored, if CONFALANA_SETTINGS '
        'environment variable is set correctly.'
    )
)
def main(
        config_file: Optional[str]
) -> int:
    """ Execute confalana script

    Args:
        config_file: App config

    Returns:
        Exit status code

    """
    if config_file:
        _config = load_config(config_file)
    else:
        _config = load_config(
            str(Path(__file__).parent.parent / 'settings.ini')
        )
    app = App.from_config(_config)
    status = app.run().exit_code(app.mode)
    if status != 0:
        make_echo('Validation error!', underline=True, style='err')()
    else:
        make_echo('Huge success!', underline=True, style='scs')()
    return status
