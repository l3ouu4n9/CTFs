#!/usr/bin/env python3

import bashlex
import os
import subprocess
import sys

ALLOWED_COMMANDS = ['ls', 'pwd', 'id', 'exit']

def validate(ast):
    queue = [ast]
    while queue:
        node = queue.pop(0)
        if node.kind == 'command':
            first_child = node.parts[0]
            if first_child.kind == 'word':
                if first_child.parts:
                    print(f'Forbidden top level command')
                    return False
                elif first_child.word.startswith(('.', '/')):
                    print('Path components are forbidden')
                    return False
                elif first_child.word.isalpha() and \
                        first_child.word not in ALLOWED_COMMANDS:
                    print('Forbidden command')
                    return False
        elif node.kind == 'commandsubstitution':
            print('Command substitution is forbidden')
            return False
        elif node.kind == 'word':
            if [c for c in ['*', '?', '['] if c in node.word]:
                print('Wildcards are forbidden')
                return False
            elif 'flag' in node.word:
                print('flag is forbidden')
                return False
        
        # Add node children
        if hasattr(node, 'parts'):
            queue += node.parts
        elif hasattr(node, 'list'):
            # CompoundNode
            queue += node.list
    return True

while True:
    inp = input('> ')

    try:
        parts = bashlex.parse(inp)
        valid = True
        for p in parts:
            if not validate(p):
                valid = False
    except:
        print('ERROR')
        continue

    if not valid:
        print('INVALID')
        continue

    subprocess.call(['bash', '-c', inp])
