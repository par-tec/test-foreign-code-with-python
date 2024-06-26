import os
from pathlib import Path

import jpype
import pytest
from jpype import shutdownJVM, startJVM

TESTDIR = Path(__file__).parent


@pytest.fixture(scope="session", autouse=False)
def setupJVM():
    """
    Setup a JVM configured to use the Europe/Rome timezone.
    """
    os.environ["TZ"] = "Europe/Rome"
    startJVM(
        convertStrings=False,
        classpath=[(TESTDIR / "guava-28.2-android.jar").as_posix()],
    )
    yield
    shutdownJVM()


def test_guava_ascii(setupJVM):
    Ascii = jpype.JClass("com.google.common.base.Ascii")
    assert Ascii.toLowerCase("EuroPython") == "europython"


@pytest.mark.parametrize(
    "inet_addr,is_valid",
    [
        ("1.2.3.4", True),
        ("3ffe::1", True),
        ("3ffe::1z", False),
        ("333.1.1.1", False),
    ],
)
def test_InetAddress(setupJVM, inet_addr, is_valid):
    InetAddress = jpype.JClass("com.google.common.net.InetAddresses")
    assert InetAddress.isInetAddress(inet_addr) == is_valid


def test_automatic_imports(setupJVM):
    import jpype.imports  # noqa

    jpype.JPackage("java")
    from java.lang import String

    assert String.format("Hello, %s", "World") == "Hello, World"


def test_bigdecimal(setupJVM):
    BigDecimal = jpype.JClass("java.math.BigDecimal")
    a, b = 0.1, 0.2
    c = a + b
    j_a = BigDecimal(a)
    j_b = BigDecimal(b)
    j_c = j_a.add(j_b)

    # BigDecimal addition is different from float addition.
    assert j_c != BigDecimal(c)

    # We can compare the string representation of the two numbers.
    assert j_c.toString()[:10] == BigDecimal(c).toString()[:10]

    # They eventually differ after the some decimals.
    assert j_c.toString() != BigDecimal(c).toString()
