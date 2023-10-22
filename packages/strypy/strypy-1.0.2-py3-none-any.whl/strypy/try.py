from basics import *
from file import *
from clipboard import *
from generator import *
from sorting import *
from colour import *

print(add("Hello","World",spaces=True)+fcolour(" abc","RED")+" my")
print(join(["hello","my","world"],spaces = True))
print(split("hello my world"))
print(switch("Helmy World","my","lo"))
print(switchchars("heLlo world","l","o"))
print(reverse("hello world"))
f = fcolour("Hello World", "BLUE")
print(bcolour(f, "BLACK"))
print(chars("Hello world"))
#print(getstrings("/home/thomaspi/tests.txt"))
#print(getchars("/home/thomaspi/tests.txt"))
print(switchdex("Hello World",3,"a"))
print(mesh("Hello","World"))
print(numcode("hello world"))
print(alphasort("Hello World"))
print(splitdex("Hello World",3))
#print(read("/home/thomaspi/tests.txt"))
print(subtract("Hello World my",3))
print(divchunks("hello world",2))
print(uniques("Hello World"))
print(unidec("abc'@¬¬!"))
print(randstr())
print(count("l","Hello World"))
copy("Hello World")
paste(True)
print(casesort("HEllo woRLd",List=False))
print(unihex("abc"))
print(unioct("abc"))