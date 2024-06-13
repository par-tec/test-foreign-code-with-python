import os
import pytest
import jpype
from jpype import startJVM, shutdownJVM


@pytest.fixture(scope="session", autouse=False)
def setupJVM():
    """
    Setup a JVM configured to use the Europe/Rome timezone.
    """
    os.environ["TZ"] = "Europe/Rome"
    startJVM(
        convertStrings=False,
        classpath=["java-project/target/guava-28.2-android.jar"],
        )
    yield
    shutdownJVM()


def test_guava_ascii(setupJVM):
    Ascii = jpype.JClass("com.google.common.base.Ascii")
    assert Ascii.toLowerCase("EuroPython") == "europython"


@pytest.mark.parametrize("inet_addr,is_valid", [
    ("1.2.3.4", True),
    ("3ffe::1", True),
    ("3ffe::1z", False),
    ("333.1.1.1", False),
])
def test_InetAddress(setupJVM, inet_addr, is_valid):
    InetAddress = jpype.JClass("com.google.common.net.InetAddresses")
    assert InetAddress.isInetAddress(inet_addr) == is_valid


def test_automatic_imports(setupJVM):
    java = jpype.JPackage("java")
    from java.lang import String

    assert String.format("Hello, %s", "World") == "Hello, World"


def test_bigdecimal(setupJVM):
    BigDecimal = jpype.JClass("java.math.BigDecimal")
    a, b = 0.1, 0.2
    b_a = BigDecimal(a)
    b_b = BigDecimal(b)
    assert b_a.add(b_b) == BigDecimal(a+b)
    raise ValueError("This test is expected to fail")