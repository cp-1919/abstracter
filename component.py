import typing as t
import warnings


class Component:
    def __init__(self, name: str, version: int, system: str = '', dependency: object = {}):
        self.name = name
        self.version = version
        self.system = system
        self.dependency = dependency
        self.general_system = ''
        self.commands = {}
        self.start_method = None
        self.update_method = None
        self.ab = None

    def system(self, content: str):
        self.system = content
        if self.ab is not None:
            self.generate_system()

    def start(self, func):
        self.start_method = func

    def update(self, func):
        self.update_method = func

    def command(self, code: str, usage: object, arguments: object, result: object = None):
        def decorator(func):
            self.commands[code] = {
                'func': func,
                'usage': usage,
                'arguments': arguments,
                'result': result,
            }
        return decorator

    def generate_system(self):
        self.general_system ={
            'component': self.name,
            'usage': self.system,
            'commands': {}
        }
        for comm in self.commands:
            self.general_system['commands'][comm] = {
                'usage': self.commands[comm]['usage'],
                'arguments': self.commands[comm]['arguments'],
                'result': self.commands[comm]['result'],
            }
        # regenerate system globally
        if self.ab is not None:
            self.ab.generate_system()

    def mount(self, ab):
        self.ab = None
        self.generate_system()
        self.ab = ab
        if self.start_method is not None:
            self.start_method(ab)

    def unmount(self):
        self.ab = None

    def deregister(self, code: str):
        if code not in self.commands:
            warnings.warn(
                'Command "{}" do not exists in component "{}".'.format(code, self.name),
                DeprecationWarning,
                stacklevel=2,
            )
            return
        self.commands.pop(code)
        # regenerate system globally
        if self.ab is not None:
            self.generate_system()
