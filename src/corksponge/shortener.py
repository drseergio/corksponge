# -*- coding: utf-8 -*-
# corksponge 
#
# quick solution to make slightly less predictable short URLs
# based on http://stackoverflow.com/questions/1051949/map-incrementing-integer-range-to-six-digit-base-26-max-but-unpredictably/1052896#1052896
# this is *NOT* a security feature
#
# Copyright: 2011 Sergey Pisarenko (drseergio@gmail.com)
# Licensed under AGPL 3.0

import random


MAPPING = range(28)
MAPPING.reverse()
CHARS = 'abcdefghijklmnopqrstuvwxyz'


def id_to_code(item_id):
  return _enbase(_encode(item_id))


def code_to_id(code):
  return _decode(_debase(code))


def _encode(n):
  result = 0
  for i, b in enumerate(MAPPING):
    b1 = 1 << i
    b2 = 1 << MAPPING[i]
    if n & b1:
      result |= b2
  return result

def _decode(n):
  result = 0
  for i, b in enumerate(MAPPING):
    b1 = 1 << i
    b2 = 1 << MAPPING[i]
    if n & b2:
      result |= b1
  return result

def _enbase(x):
  n = len(CHARS)
  if x < n:
    return CHARS[x]
  return _enbase(x/n) + CHARS[x%n]

def _debase(x):
  n = len(CHARS)
  result = 0
  for i, c in enumerate(reversed(x)):
    result += CHARS.index(c) * (n**i)
  return result
