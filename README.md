##### GFF-Fomat---Python-Modules
Functions to play with GFF file

Used with Python 3.6

##### Python modules to play with GFF file
Functions are

- Dict_Pos : Create a list of dictionnaries containing a sequence name associated to a position
- Pos_to_GFF : localize SNP position in gff file to get genes in gff format containing the position*
- get_gene_in_interval : Extract all gene included in one given region
- To continue ..

  
##### Run modules on a ptyhon script :
'''
##### -*- coding: utf-8 -*-

# Charge module 
#---------------#
import sys

import os

import re

sys.path.append('PATH_TO/software/python_tools/') # path were your gff_tools.py file is located

import gff_tools

##### Run Dict_Pos function :
#-----------------------------------#
get help :

help(gff_tools.Dict_Pos)

gff_tools.Dict_Pos("PATH_TO_YOUR_POS_FILE")

# Run : get_gene_in_intervall
#-----------------------------------#
# get help
help(get_gene_in_intervall)

# Run the function
list_dict_int=get_gene_in_intervall("/Users/elise/Desktop/head_GCF_016802725.1_UNIL_Sinv_3.0_genomic.gff", "gene", "NC_052664.1", 0, 300000)

# write the result in a file
filout=open("/Users/elise/Desktop/SELECT_GCF_016802725.1_UNIL_Sinv_3.0_genomic.gff",'w')
for dictio in list_dict_int:
    list_value=list(dictio.values())
    list_join="\t".join(str(values) for values in list_value)
    print(list_join)
    filout.write(list_join)
filout.close()
'''
