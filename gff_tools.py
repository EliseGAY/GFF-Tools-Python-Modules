""" Modules to play with gff files """
'''
Author : Elise GAY (please, ask author before sharing)
Last update : 23/01/2024
Goal : Functions to play with GFF file 
Version : Used with Python 3.6
'''

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
                if (sequence in dictio.keys() and start<=dictio[sequence]<=end and (features==str(features))):
                    new_line=line_gff[:-1]+"\t"+str(dictio[sequence])+"\n"
                    line_subset.append(new_line)
    gff_in.close()
    return line_subset

#-----------------------------------------------------------#
# Extract genes in specific region
#-----------------------------------------------------------#

def get_gene_in_intervall(gff, feature, sequence, start_inter, end_inter):  
    '''
    Usage
    ------
    Extract gene/exon/mRNA.. in a interval
    Python verion 3.6

    Arguments
    ---------
    - gff file with headers : 'Sequence / source / features / start / end / others' 
         Has to be a tab separated file with 
         Col 1 : scaffold name
         Col 2 : methods
         Col 3 : features
         col 4 : start
         col 5 : end
         col 9 : all infos on the gene, with at least : ID = "feature ID", and gene = "gene_ID"
         
         example of file : 
         NC_052664.1     RefSeq  region  1       33177226        .       +       .       ID=NC_052664.1:1..33177226;Dbxref=taxon:13686;Name=1;chromosome=1;collection-date=2018-10-01;country=USA: Florida%2C Gainesville;dev-stage=pupa;gbkey=Src;genome=chromosome;isolate=M01_SB;isolation-sourype=genomic DNA;sex=male;tissue-type=whole-body
         NC_052664.1     Gnomon  gene    26781   28479   .       +       .       ID=gene-LOC105205108;Dbxref=GeneID:105205108;Name=LOC105205108;gbkey=Gene;gene=LOC105205108;gene_biotype=protein_coding
         NC_052664.1     Gnomon  mRNA    26781   28479   .       +       .       ID=rna-XM_011174403.3;Parent=gene-LOC105205108;Dbxref=GeneID:105205108,Genbank:XM_011174403.3;Name=XM_011174403.3;gbkey=mRNA;gene=LOC105205108;model_evidence=Supporting evidence includes similarity to: 1 Prote-containing protein 2-like;transcript_id=XM_011174403.3
         NC_052664.1     Gnomon  exon    26781   28186   .       +       .       ID=exon-XM_011174403.3-1;Parent=rna-XM_011174403.3;Dbxref=GeneID:105205108,Genbank:XM_011174403.3;gbkey=mRNA;gene=LOC105205108;product=KRAB-A domain-containing protein 2-like;transcript_id=XM_011174403.3
         NC_052664.1     Gnomon  exon    28254   28479   .       +       .       ID=exon-XM_011174403.3-2;Parent=rna-XM_011174403.3;Dbxref=GeneID:105205108,Genbank:XM_011174403.3;gbkey=mRNA;gene=LOC105205108;product=KRAB-A domain-containing protein 2-like;transcript_id=XM_011174403.3
         NC_052664.1     Gnomon  CDS     26781   28186   .       +       0       ID=cds-XP_011172705.3;Parent=rna-XM_011174403.3;Dbxref=GeneID:105205108,Genbank:XP_011172705.3;Name=XP_011172705.3;gbkey=CDS;gene=LOC105205108;product=KRAB-A domain-containing protein 2-like;protein_id=XP_0111
         NC_052664.1     Gnomon  CDS     28254   28479   .       +       1       ID=cds-XP_011172705.3;Parent=rna-XM_011174403.3;Dbxref=GeneID:105205108,Genbank:XP_011172705.3;Name=XP_011172705.3;gbkey=CDS;gene=LOC105205108;product=KRAB-A domain-containing protein 2-like;protein_id=XP_0111
         NC_052664.1     Gnomon  pseudogene      93875   101470  .       -       .       ID=gene-LOC105206611;Dbxref=GeneID:105206611;Name=LOC105206611;gbkey=Gene;gene=LOC105206611;gene_biotype=pseudogene;pseudo=true
         NC_052664.1     Gnomon  exon    93875   94339   .       -       .       ID=id-LOC105206611;Parent=gene-LOC105206611;Dbxref=GeneID:105206611;gbkey=exon;gene=LOC105206611;model_evidence=Supporting evidence includes similarity to: 3 Proteins%2C and 95%25 coverage of the annotated gen
     
     - feature (str) : gene / mRNA / exon all feature available in the column 3
     - sequence (str) : Scaffold name 
     - start_inter (int) : start position
     - end_inter (int) : end position
     
    command line
    -------------
    get_gene_in_intervall(gff, features, sequence, start_inter, end_inter)

    output : 
    --------
    return a list of dictionnaries containing gene infos
    See the example run to write dictionaries in output file
    '''
    
    # read gff
    gff_in=open(gff, 'r')
    # initiate variables
    list_dict=[]
    list_selected_dict=[]
    
    # read gff by line
    for line_gff in gff_in:
        list_gff=line_gff.split(sep="\t")
        # don't read uncorrect lines
        if len(list_gff)<=6 or list_gff[2] == "region":
            continue
        else:
            # create one dict by gene
            dict_gene_i = {}
            
            # create the value for the "gene id" key
            gene_ID=[x for x in list_gff[8].split(sep=";") if re.search("gene=",x)]
            
            # fill the dict by values
            list_gene_i=[["sequence", str(list_gff[0])], 
                    ["feature",str(list_gff[2])], 
                    ["start", int(list_gff[3])], 
                    ["end",int(list_gff[4])], 
                    ["gene_ID",gene_ID]]
                     
            dict_gene_i=dict(list_gene_i)
            
            # add each dict in a list
            list_dict.append(dict_gene_i)
    # close the gff file            
    gff_in.close()
    
    # get only the gene between min and max from the interval
    for dict_i in list_dict:
        if (dict_i["sequence"] == sequence and dict_i["feature"] == feature and int(start_inter)<=dict_i["end"] and int(end_inter)>=dict_i["start"]):
            list_selected_dict.append(dict_i)
    return list_selected_dict
