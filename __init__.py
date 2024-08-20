from app import Abstracter
from component import Component
from components import *


if __name__ == '__main__':
    ab = Abstracter(
        system='help me remember things',
        debug=True,
    )
    mem = Mem('test')
    ab.register(mem.component)
    ab.start()
    print(ab.general_system)
    ab.update('帮我记录一下，明天会下雨')
    ab.update('明天会发生什么？')
