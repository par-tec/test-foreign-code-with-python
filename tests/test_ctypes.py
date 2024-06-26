import ctypes
import struct
from ctypes import Structure, c_char, c_int, c_longlong, c_uint16
from pathlib import Path

import model
import pytest
import yaml

# Load libraries.
libpmc_so = Path(__file__).parent / "libpmc.so"
messages_yaml = Path(__file__).parent / "messages.yaml"
libpmc = ctypes.CDLL(libpmc_so.as_posix())
libc = ctypes.CDLL("libc.so.6")

# Load testcases.
messages = yaml.safe_load(messages_yaml.read_text())["messages"]
