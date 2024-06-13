import jpype

def test_noop():

    jpype.startJVM(jpype.getDefaultJVMPath())

    Random = jpype.JClass('java.util.Random')
    String = jpype.JClass('java.lang.String')
    System = jpype.JClass('java.lang.System')
    # Create an instance of java.util.Random
    random = Random()
    for _ in range(20):
        System.out.println(String.format("Random number: %d", random.nextInt()))

    # Shutdown the JVM
    jpype.shutdownJVM()