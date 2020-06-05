#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
f_handler = open('./data/in.log', 'r')
sys.stdin = f_handler
str = input()
print(str)