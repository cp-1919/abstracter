from app import Abstracter
from component import Component

if __name__ == '__main__':
    ab = Abstracter(
        system='help me remember things',
        config={
            'mem': {'path': "C:\\Users\\micr1\\Desktop\\test"}
        },
        debug=True,
    )
    ab.start()
    print(ab.general_system)
    ab.update('明天多云转晴')
