#!/usr/bin/python3
import sys
import time

#TODO: openpyxl remove newlines, combine lists, remove bold


def main(filename):
    #time.struct_time()
    time.strptime("30 Nov 00", "%d %b %y")
    



if len(sys.argv) < 2:
    print('Arguments error')

try:
    for i in range(1, len(sys.argv)):
        main(sys.argv[i])
except OSError:
    print('Add filename as an argument')