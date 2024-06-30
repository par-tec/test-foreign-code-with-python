from ctypes import Structure, byref, c_char, c_int, CDLL
from pathlib import Path

# Load libraries.
l_so = Path(__file__).parent.parent / "c-project" / "le.so"
le = CDLL(l_so)


class Person(Structure):
    """Based on the C struct:
    struct Person {
        int id;
        char name[20];
    };
    """
    _fields_ = [("id", c_int), ("name", c_char * 20)]


def test_parse_person():
    p = Person()
    ret = le.parse_person(b"1;John Dow", byref(p))
    assert ret == 2
    assert p.id == 1
    assert p.name == b"John Dow"


def test_is_null_safe():
    ret = le.parse_person(None, None)
    assert ret == -1