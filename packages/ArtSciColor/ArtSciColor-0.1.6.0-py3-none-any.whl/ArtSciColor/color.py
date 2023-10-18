#!/usr/bin/env python
# -*- coding: utf-8 -*-

# https://matplotlib.org/stable/api/_as_gen/matplotlib.colors.ListedColormap.html
# 

import matplotlib.colors as mcolors
from matplotlib.colors import LinearSegmentedColormap

def addHexOpacity(colors, alpha='1A'):
    return [c+alpha for c in colors]


def replaceHexOpacity(colors, alpha='FF'):
    return [i[:-2]+alpha for i in colors]


def generateAlphaColorMapFromColor(color):
    alphaMap = LinearSegmentedColormap.from_list(
        'cmap',
        [(0.0, 0.0, 0.0, 0.0), color],
        gamma=0
    )
    return alphaMap

def colorPaletteFromHexList(clist):
    c = mcolors.ColorConverter().to_rgb
    clrs = [c(i) for i in clist]
    rvb = mcolors.LinearSegmentedColormap.from_list("", clrs)
    return rvb