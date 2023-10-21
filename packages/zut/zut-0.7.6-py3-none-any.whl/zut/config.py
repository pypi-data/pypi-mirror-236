from __future__ import annotations
import os
import re

import sys
from configparser import ConfigParser, _UNSET, NoOptionError
from pathlib import Path

from .logging import _get_prog
from .text import skip_bom
from .types import to_bool


def get_config(prog: str, *, default_section: str = None, list_delimiter: str = ',') -> ExtendedConfigParser:
    """
    A function to search for configuration files in some common paths.
    """
    if not prog:
        raise ValueError("prog required")
        # NOTE: we should not try to determine prog here: this is too dangerous (invalid/fake configuration files could be loaded by mistake)

    parser = ExtendedConfigParser(default_section=default_section, list_delimiter=list_delimiter)

    parser.read([
        # System configuration
        Path(f'C:/ProgramData/{prog}.conf' if sys.platform == 'win32' else f'/etc/{prog}.conf').expanduser(),
        # User configuration
        Path(f'~/.config/{prog}.conf').expanduser(),
        # Local configuration
        "local.conf",
    ], encoding='utf-8')

    return parser


class ExtendedConfigParser(ConfigParser):
    def __init__(self, *, default_section: str = None, list_delimiter: str = ','):
        super().__init__()
        self.default_section = default_section
        self.list_delimiter = list_delimiter
        self.name_pattern = re.compile(r'^[\w\-_\:]+$')
   

    def get(self, section: str, option: str = _UNSET, *, raw=False, vars=None, fallback: str = _UNSET, try_secrets: bool = False, try_file: bool = False) -> str:
        """
        If `try_secrets` is True, will try to read the value from file `/run/secrets/{section}_{option}` if exists.
        If `try_file` is True, if the option (for example `password`) is not provided, will try to read the value from the file indicated by the option `{option}_file` (for example `password_file`).
        """
        if option == _UNSET:
            if not self.default_section:
                raise ValueError('section and option must both be set (no default_section provided)')
            option = section
            section = self.default_section

        if not self.name_pattern.match(option):
            raise ValueError(f'invalid option characters: {option}')

        if not self.name_pattern.match(section):
            raise ValueError(f'invalid section characters: {section}')

        # try secrets
        if try_secrets:
            secret_name = f'{section}_{option}'.replace(':', '-')
            secret_path = f'/run/secrets/{secret_name}'
            if os.path.exists(secret_path):
                return _read_file_and_rstrip_newline(secret_path)

        # try option
        try:
            return super().get(section, option, raw=raw, vars=vars)
        except NoOptionError:            
            if not try_file:                
                if fallback is _UNSET:
                    raise
                else:
                    return fallback
                
        # try file
        try:
            path = super().get(section, f'{option}_file', raw=raw, vars=vars)
            return _read_file_and_rstrip_newline(path)
        except NoOptionError:  
            if fallback is _UNSET:
                raise
            else:
                return fallback


    def getlist(self, section: str, option: str = _UNSET, *, raw=False, vars=None, fallback: list[str] = _UNSET, try_secrets: bool = False, try_file: bool = False) -> list[str]:
        values_str = self.get(section, option, raw=raw, vars=vars, fallback=fallback, try_secrets=try_secrets, try_file=try_file)
        if not isinstance(values_str, str):
            return values_str # fallback
        
        values = []
        for value in values_str.split(self.list_delimiter):
            value = value.strip()
            if not value:
                continue
            values.append(value)

        return values
    

    def getint(self, section: str, option: str = _UNSET, *, raw=False, vars=None, fallback: int = _UNSET, try_secrets: bool = False, try_file: bool = False) -> int:
        value = self.get(section, option, raw=raw, vars=vars, fallback=fallback, try_secrets=try_secrets, try_file=try_file)
        if not isinstance(value, str):
            return value # fallback
        return int(value)
    

    def getfloat(self, section: str, option: str = _UNSET, *, raw=False, vars=None, fallback: int = _UNSET, try_secrets: bool = False, try_file: bool = False) -> float:
        value = self.get(section, option, raw=raw, vars=vars, fallback=fallback, try_secrets=try_secrets, try_file=try_file)
        if not isinstance(value, str):
            return value # fallback
        return float(value)
    

    def getboolean(self, section: str, option: str = _UNSET, *, raw=False, vars=None, fallback: bool = _UNSET, try_secrets: bool = False, try_file: bool = False) -> bool:
        value = self.get(section, option, raw=raw, vars=vars, fallback=fallback, try_secrets=try_secrets, try_file=try_file)
        if not isinstance(value, str):
            return value # fallback
        return to_bool(value)


def _read_file_and_rstrip_newline(path: os.PathLike):
    with open(path, 'r', encoding='utf-8') as fp:
        skip_bom(fp)
        value = fp.read()
        return value.rstrip('\r\n')
