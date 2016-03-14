#!/bin/sh

g++ -O3 -I$HOME/sw/include gentryextended.cpp gentryprivkeys.cpp gentrypubkeys.cpp testGentry.cpp -o test_gentry -L$HOME/sw/lib -lntl -lgmp -lm
