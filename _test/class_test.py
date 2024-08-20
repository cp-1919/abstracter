def deco(func):
    func()


class T:
    def __init__(self):
        self.name = 'joe'
        @deco
        def test():
            print(self.name)

T()