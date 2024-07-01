from ctypes import CDLL, Structure, byref, c_char, c_int
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


#
# $ ulimit -c unlimited
# $ pytest -k null_safe
# Segmentation fault (core dumped)
#
def test_is_null_safe():
    ret = le.parse_person(None, None)
    assert ret == -1


from ctypes import *
from ctypes import POINTER, Structure, c_int
from pathlib import Path

# Load libraries.
cJSON_so = Path(__file__).parent / "libcjson.so"
lc = CDLL(cJSON_so)


#
# Define cJSON struct in two steps to avoid circular references.
#
class cJSON(Structure):
    pass


cJSON._fields_ = [
    ("next", POINTER(cJSON)),
    ("prev", POINTER(cJSON)),
    ("child", POINTER(cJSON)),
    ("type", c_int),
    ("valuestring", c_char_p),
    ("valueint", c_int),
    ("valuedouble", c_double),
    ("string", c_char_p),
]
#
# Associate a return type with cJSON_Parse.
#
cJSON_Parse = lc.cJSON_Parse
cJSON_Parse.restype = POINTER(cJSON)
