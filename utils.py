'''
os.environ['SAMPLE'] = """
...
"""
inp = get_input()
or
inp = get_input('input.txt')
'''
import os
import textwrap

def get_input(file=None):
    if file:
        inp = open(file).read().split("\n")
    else:
        inp = textwrap.dedent(os.environ['SAMPLE']).split("\n")
    if inp[0] == "":
        inp = inp[1:]
    if inp[-1] == "":
        inp = inp[:-1]
    return inp
