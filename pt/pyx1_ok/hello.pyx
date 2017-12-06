cimport cython
import pandas as pd
def say_hello_to(name):
    print("Hello %s!" % name)

cdef struct AB:
    char *c
    int a
    int b

def StructTest():
    cdef AB carr[100000]
    #cdef AB ab
    #ab.a = 1
    #ab.b = 2
    for i in range(0,100000):
        carr[i].c = "a00000000000000000000000008888888uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuubc"
        carr[i].a = 1
        carr[i].b = 2

    return carr
    #return ab
