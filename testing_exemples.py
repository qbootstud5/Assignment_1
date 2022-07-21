#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wednesday July 20
@author: Jon Oillarburu

This file solves the Assignment 1
"""

import math

from plot_functions import plot


def example_1():
    scale = 0.1
    n = int(8 * math.pi / scale)
    x = [scale * i for i in range(n)]
    y = [math.sin(scale * i) for i in range(n)]
    plot(x, y,
         display_grid=True,
         height=15,
         title="The sine function",
         legend="f(x) = sin(x), where 0 <= x <= 8π")


def example_2():
    scale = 0.1
    n = int(2 * math.pi / scale)
    x = [scale * i for i in range(n)]
    y = [math.cos(scale * i) for i in range(n)]
    plot(x, y,
         width=50,
         title="The cosine function",
         legend="f(x) = cos(x), where 0 <= x <= 2π")


def example_3():
    y = [ord(c) for c in 'ASCII Plotter example']
    n = len(y)
    x = [i for i in range(n)]
    plot(x, y,
         title="Plotting Random Data", legend="f(x) = random data")


def main():
    example_1()
    example_2()
    example_3()


if __name__ == "__main__":
    main()
