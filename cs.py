#!/usr/bin/env python3
import os
from re import finditer

print('Code Size')


def is_hidden(root, file):
    if file.startswith('.'):
        return True
    return len([d for d in root.split(os.sep)[1:] if d.startswith('.')]) > 0


def get_headers(code: str):
    result = []
    for match in finditer(r'\bdef\b', code):
        result.append(match)
    return result


def get_bodies(code: str):
    lines = code.split('\n')
    for line in lines:
        print(line)


def scan(path: str):
    for root, dirs, files in os.walk(path):
        for file in files:
            if is_hidden(root, file):
                continue
            if file.lower().endswith('.py'):
                with open(os.path.join(root, file)) as f:
                    contents = f.read()
                print(get_headers(contents))
                get_bodies(contents)


scan('.')
