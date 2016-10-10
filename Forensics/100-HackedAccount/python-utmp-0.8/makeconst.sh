#!/bin/sh

gcc -Wall -pedantic makeconst.c $* -o makeconst
./makeconst > UTMPCONST.py

