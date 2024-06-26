import ctypes
from ctypes import Structure, byref, c_char, c_int, create_string_buffer
from pathlib import Path

# Load libraries.
l_so = Path(__file__).parent.parent / "c-project" / "libexample.so"
libc = ctypes.CDLL("libc.so.6")
libexample = ctypes.CDLL(l_so)


class Person(Structure):
    _fields_ = [("id", c_int), ("name", c_char * 20)]


def test_parse_person():
    p = Person()
    row = "1;John Dow"
    row_p = create_string_buffer(row.encode())
    libexample.parse_person(row_p, byref(p))
    assert p.id == 1
    assert p.name == b"John Dow"
