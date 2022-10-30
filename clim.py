#!/usr/bin/env python3
import os

from codelimit.Python import get_blocks, get_headers
from codelimit.Scope import build_scopes

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
            if file.lower().endswith('.py'):
                print(f'== {file}')
                with open(os.path.join(root, file)) as f:
                    code = f.read()
                headers = get_headers(code)
                blocks = get_blocks(code)
                scopes = build_scopes(headers, blocks)
                for scope in scopes:
                    print(f'{file}#{scope.header.start.line}: {scope.block.end.line - scope.block.start.line + 1}')


scan('.')
