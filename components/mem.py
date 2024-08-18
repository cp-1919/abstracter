from __init__ import Component
import json
import os

system = '''
You are a people who easily forgot things, thus you have to record what you do now.
mem helps you remember things with note.
You can create note with profile, which help you remember.
Remember: You could not read note that not exists.
'''
component = Component('mem', 0, system)
path = None
files = []

profiles = {}
contents = {}


@component.start
def start(ab):
    if 'path' in ab.config:
        path = ab.config['path']
        if path[-1] == '/' or path[-1] == '\\':
            path += '/'


@component.update
def update(ab):
    return 'your notes:' + json.dumps(profiles, indent=2)


@component.command(
    code='read',
    usage='read data in note',
    arguments={
        'note': 'note name'
    },
    result={
        'note': 'note name',
        'content': 'content of note',
    }
)
def mem_read(args):
    return {
        'file': args['note'],
        'content': contents[args['note']]
    }


@component.command(
    code='write',
    usage='write or rewrite note',
    arguments={
        'note': 'note name',
        'profile': 'note profile',
        'content': 'content of note'
    }
)
def mem_write(args):
    profiles[args['note']] = args['profile']
    contents[args['note']] = args['content']
