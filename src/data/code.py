#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
f_handler = open('./data/in.log', 'r')
sys.stdin = f_handler
#author: wr786

print("Hello, My Happy World!")

str = """
POPIPA
PIPOPA
POPIPAPAPIPOPA!
"""

def fn():
    print(str)
    
fn()