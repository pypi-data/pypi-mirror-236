from jnius import autoclass
System=autoclass('java.lang.System')
System.out.println("Hello World!")