from component import Component

system = '''
Basic commands that commonly used.
'''
component = Component('basic', 0, system)
ab = None


@component.start
def start(__ab):
    ab = __ab


@component.command(
    code='exit',
    usage='if you have already achieved user\'s goal, or do not get any request, call exit to stop',
    arguments={
        'result': 'report to user'
    }
)
def ab_exit(args):
    ab.is_update = False
