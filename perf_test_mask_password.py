#!/usr/bin/env python

from __future__ import print_function

import timeit

import strutils

# A moderately sized input (~50K) string
# http://paste.openstack.org/raw/155864/
infile = 'sample.json'

with open(infile, 'r') as f:
    input_str = f.read()
print('payload has %d bytes' % len(input_str))

times = []

for pattern in strutils._SANITIZE_PATTERNS_2:
    print('\ntesting %s' % pattern.pattern)
    t = timeit.Timer(
        "re.sub(pattern, r'\g<1>***\g<2>', payload)",
        """
import re
payload = '''%s'''
pattern = re.compile(r'''%s''')
""" % (input_str, pattern.pattern))
    result = t.timeit(1)
    print(result)
    times.append((result, pattern.pattern))

print('\nslowest to fastest:')
times = reversed(sorted(times))
for t in times:
    print('%s - %s ' % t)

print('\ntesting all patterns')
t = timeit.Timer(
    "strutils.mask_password('''" + input_str + "''')",
    "import strutils",
)
print(t.timeit(1))
