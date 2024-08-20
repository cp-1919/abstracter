import ollama
import config as abconfig
from string import Template
import warnings
import json
from component import Component


class Abstracter:
    def __init__(
            self,
            system: str = '',
            config: object = None,
            model: str = 'gemma2:9b',
            debug: bool = False,
    ):
        self.system = system
        self.config = config
        self.model = model
        self.debug = debug
        self.general_system = ''
        self.commands = {}
        self.components = {}
        # status
        self.is_update = False

    def chat(self, messages: list) -> object:
        return ollama.chat(model=self.model, messages=messages, stream=False)['message']

    def register(self, comp: Component):
        if comp.name not in self.components:
            self.components[comp.name] = comp
            comp.mount(self)
        else:
            warnings.warn(
                'Component named "{}" has already exists.'.format(comp.name),
                DeprecationWarning,
                stacklevel=2,
            )
            return

    def start(self):
        self.generate_system()
        # call start methods of all components
        for comp in self.components:
            if self.components[comp].start_method is not None:
                self.components[comp].start_method(self)

    def update(self, request: str):
        # init
        # call update methods of all components
        res_updates = {}
        for comp in self.components:
            if self.components[comp].update_method is not None:
                res_updates[comp] = self.components[comp].update_method(self)
        messages = [
            {'role': 'system', 'content': self.general_system},
            {
                'role': 'user',
                'content': Template(abconfig.ab_update_template).substitute({
                    'header': json.dumps(res_updates),
                    'request': request
                })
            }
        ]
        # set status
        self.is_update = True
        while self.is_update:
            res_msg = self.chat(messages)
            messages.append(res_msg)
            if self.debug:
                print(res_msg)
            json_str = res_msg['content'].split('```json\n')[-1].split('\n```')[0]
            commands = json.loads(json_str)
            if commands == {}:
                self.is_update = False
                break
            result = {'warnings': []}
            # parse the call of commands
            for calls in commands:
                [comp, comm] = calls.split('.')
                if comp not in self.components:
                    result['warnings'].append('component named "{}" do not exists'.format(comp))
                if comm not in self.components[comp].commands:
                    result['warnings'].append('command named "{}" do not exists in component "{}"'.format(comm, comp))
                if self.components[comp].commands[comm]['result'] is None:
                    for args in commands[calls]:
                        self.components[comp].commands[comm]['func'](args)
                else:
                    result[calls] = []
                    for args in commands[calls]:
                        result[calls].append(self.components[comp].commands[comm]['func'](args))
                messages.append({'role': 'user', 'content': json.dumps(result)})

    def generate_system(self):
        # get systems of components
        comp_sys = {}
        for comp in self.components:
            comp_sys[comp] = self.components[comp].general_system
        self.general_system = Template(abconfig.ab_system_template).substitute({
            'role': self.system,
            'components': json.dumps(comp_sys, indent=2)
        })

    def copy(self):
        ab = Abstracter(
            system=self.system,
            model=self.model,
            debug=self.debug,
        )
        return ab
