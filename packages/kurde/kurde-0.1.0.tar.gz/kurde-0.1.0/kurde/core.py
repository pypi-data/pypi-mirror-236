import os
import sys
import re
import addict
import simplenum
import builtins
import orjson
import plumbum
from pathlib import Path
from pygments import highlight, lexers, formatters

builtins.Dict = addict.Dict
builtins.Enum = simplenum.Enum
builtins.enum = simplenum
builtins.env = Dict(**os.environ)
builtins.Path = Path
builtins.cmd = plumbum.local.cmd
builtins.re = re

ROOT_NAME = 'ROOT'
JSON_SERIALIZABLE = (type(None), int, float, bool, str, list, tuple, set, dict, Enum, Path)

def serialize(script_path):
    script_path = Path(script_path)
    code = script_path.read_text()

    os.chdir(script_path.parent)
    glo = {'__file__': str(script_path)}
    loc = {}
    exec(code, glo, loc)

    if ROOT_NAME in loc:
        payload = loc[ROOT_NAME]
    else:
        payload = {k: v for k, v in loc.items() if isinstance(v, JSON_SERIALIZABLE)}

    json_bytes = orjson.dumps(payload, default=json_encode_extra, option=orjson.OPT_INDENT_2)
    json_text = json_bytes.decode().strip()
    if sys.stdout.isatty():
        json_text = highlight(json_text.encode('utf8'), lexers.JsonLexer(), formatters.TerminalFormatter()).strip()
    print(json_text)

def json_encode_extra(obj):
    if isinstance(obj, set):
        return tuple(obj)

    if isinstance(obj, Enum):
        return obj.value

    if isinstance(obj, Path):
        return str(obj)

    raise TypeError
