#!/usr/bin/env python3
import os

from sourcelimit.Python import get_blocks, get_headers

print('Source Limit')


def is_hidden(root, file):
    if file.startswith('.'):
        return True
    return len([d for d in root.split(os.sep)[1:] if d.startswith('.')]) > 0


def scan(path: str):
    for root, dirs, files in os.walk(path):
        for file in files:
            if is_hidden(root, file):
                continue
            if file.lower().endswith('.py'):
                print(f'== {file}')
                with open(os.path.join(root, file)) as f:
                    contents = f.read()
                print('==== Headers')
                print(get_headers(contents))
                print('==== Blocks')
                print(get_blocks(contents))


scan('.')
