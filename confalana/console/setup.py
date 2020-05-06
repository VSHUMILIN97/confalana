""" Confalana setup utilities """
from configparser import ConfigParser, Error as ConfigParserError
from os import getenv, path
from pathlib import Path
from typing import Union, Callable, Tuple, Iterable

from confalana.console.messaging import make_echo
from confalana.exceptions import InvalidConfigurationError


def load_config(file_path: str) -> ConfigParser:
    """ Parse settings.ini file

    Args:
        file_path: Viable path

    Returns:
        Initialised app config
    """
    conf_chain: Iterable[Tuple[str, Callable[[], None]]] = (
        (
            getenv('CONFALANA_SETTINGS', path.curdir),
            make_echo('Cannot retrieve config from ENV variable.')
        ),
        (
            file_path,
            make_echo(
                f'{file_path} contain invalid configuration. '
                f'Is this intentional?',
                style='err'
            )
        )
    )
    for entry, callback in conf_chain:
        try:
            _parse_cfg(entry, callback)
        except InvalidConfigurationError:
            continue

    return _parse_cfg(
        str(Path(__file__).parent.parent / 'settings.ini'),
        make_echo('Using default settings.ini')
    )


def _parse_cfg(
        path_: Union[str, Path],
        echo_message: Callable[[], None],
) -> ConfigParser:
    """ TODO:

    Args:
        path_:
        echo_message:

    Returns:

    """
    conf_path = Path(path_)
    config = ConfigParser()
    if conf_path.exists() and conf_path.is_file():
        try:
            config.read_file(conf_path.open())
            return config
        except ConfigParserError:
            echo_message()
    raise InvalidConfigurationError()
