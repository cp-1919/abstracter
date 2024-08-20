import components.mem as mem
mem.path = 'match'

from _test.reimport_test2 import mem as mem2
print(mem2.path)
