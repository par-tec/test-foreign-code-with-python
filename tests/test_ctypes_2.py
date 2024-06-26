import ctypes
import json
from ctypes import *
from ctypes import POINTER, Structure, c_int
from pathlib import Path

import pytest

# Load libraries.
cJSON_so = Path(__file__).parent / "libcjson.so"
libc = ctypes.CDLL("libc.so.6")
libcjson = ctypes.CDLL(cJSON_so)


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
cJSON_Parse = libcjson.cJSON_Parse
cJSON_Parse.restype = ctypes.POINTER(cJSON)


@pytest.mark.parametrize(
    "json_document, json_type, expected_values",
    [
        (b"1", 1 << 3, 1),
        (b"1.1", 1 << 3, 1.1),
        (b"1e+2", 1 << 3, 100),
        (b"1_000", 1 << 3, 1.0),
    ],
)
def test_cJSON_Parse_can_parse_numbers(json_document, json_type, expected_values):
    msg = ctypes.create_string_buffer(json_document)
    c_json = cJSON_Parse(msg)
    assert c_json.contents.type == json_type
    assert c_json.contents.valuedouble == expected_values


@pytest.mark.parametrize(
    "json_document, json_type, expected_values",
    [
        (b'"ciao"', 1 << 4, b"ciao"),
        (json.dumps("però").encode(), 1 << 4, "però".encode()),
    ],
)
def test_cJSON_Parse_can_parse_strings(json_document, json_type, expected_values):
    msg = ctypes.create_string_buffer(json_document)
    c_json = cJSON_Parse(msg)
    assert c_json.contents.type == json_type
    assert c_json.contents.valuestring == expected_values


@pytest.mark.parametrize(
    "json_document, json_type, expected_values",
    [
        (b"[1,2,3]", 1 << 5, [1, 2, 3]),
    ],
)
def test_cJSON_Parse_can_parse_arrays(json_document, json_type, expected_values):
    msg = ctypes.create_string_buffer(json_document)
    c_json = cJSON_Parse(msg)
    assert c_json.contents.type == json_type

    e = c_json.contents.child.contents
    for expected_value in expected_values:
        assert e.valueint == expected_value
        try:
            e = e.next.contents
        except ValueError:
            assert expected_value == expected_values[-1]
            break


@pytest.mark.parametrize(
    "json_document, json_type, expected_values",
    [
        (b'{"a": 1', None, None),
    ],
)
def test_cJSON_Parse_raises_when_invalid_json(
    json_document, json_type, expected_values
):
    msg = ctypes.create_string_buffer(json_document)
    c_json = cJSON_Parse(msg)
    with pytest.raises(ValueError):
        assert c_json.contents
