import ctypes
from ctypes import Structure, byref, c_char, c_uint
from pathlib import Path
from string import ascii_letters

from hypothesis import given
from hypothesis import strategies as st

# Load libraries.
l_so = Path(__file__).parent.parent / "c-project" / "le.so"
libc = ctypes.CDLL("libc.so.6")
le = ctypes.CDLL(l_so)


class Person(Structure):
    _fields_ = [("id", c_uint), ("name", c_char * 20)]


@given(
    id_=st.integers(min_value=0, max_value=2**32 - 1),
    name=st.text(ascii_letters + " ", min_size=1, max_size=19),
)
def test_parse_person(id_, name):
    raw_data = f"{id_};{name}".encode()
    p = Person()
    le.parse_person(raw_data, byref(p))
    assert p.id == id_
    assert p.name == name.encode()


@given(
    id_=st.integers(min_value=0),
    name=st.text(min_size=19, max_size=50),
)
def test_dont_accept_malformed_strings(id_, name):
    raw_data = f"{id_};{name}".encode()
    p = Person()
    ret = le.parse_person(raw_data, byref(p))
    assert ret == -1
