#!/usr/bin/env python3

ifield = 0

sudoku = []

f = open('input.txt', 'r')
while ifield < 36:
    # skip "Field"
    f.readline().strip()

    field = []
    for i in range(6):
        line = f.readline().strip().split(' ')
        field.append(line)
    sudoku.append(field)

    # skip empty line
    f.readline().strip()

    ifield += 1

f.close()


def print_characters():
    for ifield in range(36):
        for y in range(6):
            for x in range(6):
                print(sudoku[ifield][y][x])

# print_characters()
# ./solution.py | sort  | uniq
abc = set([c for c in '_{}0123456abcdefghijklmnopqrstuvwxyz'])


def print_sudoku():
    for ifield in range(36):
        print('Field', ifield)
        for y in range(6):
            for x in range(6):
                print(sudoku[ifield][y][x], end='')
            print()
        print()


stars_are_there = True
while stars_are_there:
    stars_are_there = False
    for ifield in range(36):
        for y in range(6):
            for x in range(6):
                if sudoku[ifield][y][x] == '*':
                    stars_are_there = True

                    # look for possible variants within the same field
                    written = set()
                    for yy in range(6):
                        for xx in range(6):
                            v = sudoku[ifield][yy][xx]
                            if v != '*':
                                written.add(v)
                    available_in_field = abc - written

                    # look for possible variants within the same column
                    written = set()
                    for iifield in range(36):
                        v = sudoku[iifield][y][x]
                        if v != '*':
                            written.add(v)
                    available_in_column = abc - written

                    # print(ifield, y, x, available_in_field, available_in_column)
                    available = available_in_column.intersection(available_in_field)
                    # print(ifield, y, x, available)
                    if len(available) == 1:
                        sudoku[ifield][y][x] = available.pop()

print_sudoku()