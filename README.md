# GFF-Fromat---Python-Modules
Functions to play with GFF file 
Used with Python 3.6

# Python modules to play with GFF file
Functions are
- Dict_Pos : Create a list of dictionnaries containing a sequence name associated to a position
- Pos_to_GFF : localize SNP position in gff file to get genes in gff format containing the position
- To be continue ..

  
# Run modules on a ptyhon script :
'''
##### -*- coding: utf-8 -*-

import sys
import os
import re

sys.path.append('PATH_TO/software/python_tools/')

import gff_tools

##### example of one function used :

get help :

help(gff_tools.Dict_Pos)

gff_tools.Dict_Pos("PATH_TO_YOUR_POS_FILE")

'''
