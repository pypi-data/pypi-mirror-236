#!/usr/bin/env python
# -*- coding: utf-8 -*-

import warnings
import pandas as pd
import pkg_resources
from os.path import join
import ArtSciColor.paths as pth
import ArtSciColor.auxiliary as aux

SWATCH_DIMS = {'width': 750, 'height': 50}
NOT_ART = set(('Splatoon', 'Ghibli'))
CATEGORIES = {
    'Art': set(("Nolde", "Warhol", "Monet", "Kirchner", "Miro", "Picasso")),
    'Movies': set(('Ghibli', )),
    'Gaming': set(('Splatoon', )),
    'Other': set(('chipdelmal', 'coolors'))
}
ARTISTS_SET = set.union(*list(CATEGORIES.values()))
DF_SORTING = (
    'artist', 'title', 'palette', 'hash', 
    'clusters', 'clustering', 'url', 'filename'
)
###############################################################################
# Load Serialized data
#   https://stackoverflow.com/questions/779495/access-data-in-package-subdirectory
#   https://packaging.python.org/en/latest/guides/distributing-packages-using-setuptools/
###############################################################################
DATA_PATH = pkg_resources.resource_filename('ArtSciColor', 'data/')
(PT_SW, PT_DF) = (join(DATA_PATH, 'SWATCHES.bz'), join(DATA_PATH, 'DB.csv'))
try:
    SWATCHES = aux.loadDatabase(PT_SW, df=False)
    SWATCHES_DF = pd.read_csv(PT_DF)
except:
    warnings.warn("Missing colors database!")
###############################################################################
# HTML/MD Text
###############################################################################
RDM_HEADER = [
    f'<th style="text-align: center; vertical-align: middle;">{e}</th>'
    for e in ('Artist', 'Title', 'Palette', 'ID') # , 'Hex Palette')
]
RDM_TEXT = '''
<!DOCTYPE html>
<html><body>
<h1>{}</h1>
<table style="width:100%">
<tr>{}</tr>{}
</table>
</body></html>
'''
def generateHTMLEntry(artist, url, title, relPth, hname, strPal):
    entry = [
        f'<td style="text-align: center; vertical-align: middle;">{e}</td>'
        for e in (
            f'<p style="font-size:14px">{artist}</p>', # Artist
            f'<a href={url} style="font-size:14px">{title}</a>', # URL, Title 
            f'<img style="border-radius: 14px;" src="{relPth}" height="25">', # Relative Path 
            f'<p style="font-size:14px">{hname}</p>', # Hash Name
            # f'<p style="font-size:14px">{strPal}</p>' # String Palette
        )
    ]
    mdRow = '\r<tr>'+' '.join(entry)+'</tr>'
    return mdRow