#!/usr/bin/env python3
import os

from sourcelimit.Python import get_blocks, get_headers
from sourcelimit.Source import get_range

print('Code Limit')


def is_hidden(root, file):
    if file.startswith('.'):
        return True
    return len([d for d in root.split(os.sep)[1:] if d.startswith('.')]) > 0


def scan(path: str):
    for root, dirs, files in os.walk(path):
        for file in files:
            if is_hidden(root, file):
                continue
            if file.lower().endswith('.py') and file == 'clim.py':
                print(f'== {file}')
                with open(os.path.join(root, file)) as f:
                    code = f.read()
                print('==== Headers')
                for h in get_headers(code):
                    print(h)
                    print(get_range(code, h))
                print('==== Blocks')
                print(get_blocks(code))


scan('.')
