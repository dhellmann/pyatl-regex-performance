#!/usr/bin/env python

from __future__ import print_function

import timeit

infile = 'sample.json'

with open(infile, 'r') as f:
    input_str = f.read()

t = timeit.Timer(
    "re.sub(pattern, r'\g<1>***\g<2>', payload)",
    """
import re
payload = '''%s'''
pattern = re.compile(r'admin_pass')
""" % input_str)
print('regex  : %10.10f' % t.timeit(5))

t = timeit.Timer(
    "'admin_pass' in payload",
    "payload = '''%s'''" % input_str,
)
print('literal: %10.10f' % t.timeit(5))
