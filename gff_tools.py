""" Modules to play with gff files """

#!/usr/local/bin/python
# -*- coding: utf-8 -*-

#------------------------#
# Import modules
#------------------------#
import sys
import re

#-----------------------------------------------------------#
# Associate position with sequences (contig, chr, scaffold)
#-----------------------------------------------------------#

def Dict_Pos(position_file):
    '''
    Usage
    ------
    Create a list of dictionnaries containing a sequence name associated to a position
    Python verion 3.6

    Arguments
    ---------
    - Postion file with two column : sequence / position

    command line
    -------------
    Get_Pos(position_file)

    output : dictionnary with key=sequence and value=position
    --------

    '''
    pos_dict = {}
    list_dict=[]
    pos_in=open(position_file, 'r')
    for line_pos in pos_in:
        line_pos_split=line_pos.split("\t")
        sequence=str(line_pos_split[0])
        position=int(line_pos_split[1])
        pos_dict[sequence]=position
        list_dict.append(pos_dict)
        pos_dict = {}
    return list_dict

#-----------------------------------------------------------#
# Extract gene containing SNP positions
#-----------------------------------------------------------#

def Pos_to_GFF(gff, list_dict, features):  
    '''
    Usage
    ------
    localize SNP position in gff file to get genes in gff format containing the position
    Python verion 3.6

    Arguments
    ---------
    - gff file with header 'Sequence / source / features / start / end / others' 
     and has to be a tab separated file
    - A list of dictionnaries containing a sequence name associated to a position
      pos_dict : dictionnary with key=sequence and value=position. See the function 'Dict_Pos'
    - feature : which line you want to extract from the GFF : use for instance CDS, exon, Gene, RNA (3th column of your GFF file)

    command line
    -------------
    Pos_to_GFF(gff, pos_dict)

    output : List of GFF line (char) with only genes containing the positions required
    --------
    '''
    gff_in=open(gff, 'r')
    line_subset=[]
    for line_gff in gff_in:
        list_gff=line_gff.split(sep="\t")
        if len(list_gff)<5:
            continue
        else:
            sequence=str(list_gff[0])
            start=int(list_gff[3])
            end=int(list_gff[4])
            features=str(list_gff[2])
            for dictio in list_dict:
                if sequence in dictio.keys() and start<=dictio[sequence]<=end and (features==str(feature))):
                    new_line=line_gff[:-1]+"\t"+str(dictio[sequence])+"\n"
                    line_subset.append(new_line)
    gff_in.close()
    return line_subset
