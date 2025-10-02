# GFF_Tools

Author: Elise Gay (EPHE, MNHN)  
Description: A small collection of Python utilities to parse, query and export GFF3 files and to map positions (e.g. SNPs) to GFF features.

This module provides functions to read GFF files into Python structures, write BED files from GFF features, map simple position lists to GFF features, and extract features located in a genomic interval.

---

## Features

- Dict_GFF: parse a GFF3 file and return a list of dictionaries for selected features (e.g. `gene`, `mRNA`, `exon`, `CDS`).  
- Write_Bed: write selected features from a GFF to a BED-like file (chr, start, end, ID).  
- Dict_Pos: read a two-column position file (`sequence<TAB>position`) into a list of dictionaries.  
- Pos_to_GFF: return GFF lines (with appended position) that contain provided positions.  
- get_gene_in_interval: return gene/mRNA/exon features present in a specified interval on a scaffold.

---

## Installation

Clone the repo and import the module in your scripts.

```bash
git clone https://github.com/your-account/GFF_Tools.git
cd GFF_Tools
```

In Python:

```python
from Gff_Tools import Dict_GFF, Dict_Pos, Pos_to_GFF, get_gene_in_interval, Write_Bed
```

(Replace `Gff_Tools` with the actual module name/file name if different.)

---

## Usage

### 1) Parse GFF and get a list of feature dictionaries
```python
# Parse genes and mRNAs from a GFF file
results = Dict_GFF("annotations.gff3", ["gene", "mRNA"])
# results is a list of dicts like:
# {'feature': 'gene', 'start': 1234, 'end': 5678, 'chr': 'NC_000001.1', 'ID': 'gene-XYZ'}
```

### 2) Write a BED-like file from GFF features
```python
# Write a BED of genes to the current directory
Write_Bed("annotations.gff3", "gene", outdir=".")
# Output file: ./gene.bed  (columns: chr, start, end, ID)
```

### 3) Read a position file (sequence <TAB> position)
Example positions file (`positions.txt`):
```
NC_000001.1	1250
NC_000001.1	50000
scaffold_12	897
```

```python
pos_list = Dict_Pos("positions.txt")
# pos_list is a list of dicts like: [{'NC_000001.1': 1250}, {'NC_000001.1': 50000}, {'scaffold_12': 897}]
```

### 4) Map positions to GFF features
```python
# Return GFF lines that contain positions (feature filter applied, e.g. 'gene' or 'CDS')
matched_lines = Pos_to_GFF("annotations.gff3", pos_list, "gene")
# matched_lines is a list of lines (strings). Example: "NC_000001.1\tRefSeq\tgene\t1000\t2000\t.\t+\t.\tID=gene-XYZ\t1250\n"
# You can write them to a file:
with open("positions_in_genes.gff", "w") as fh:
    fh.writelines(matched_lines)
```

### 5) Extract features in a genomic interval
```python
# Get genes overlapping interval 10000-20000 on scaffold NC_000001.1
genes = get_gene_in_interval("annotations.gff3", "gene", "NC_000001.1", 10000, 20000)
# genes is a list of dicts each containing keys: sequence, feature, start, end, gene_ID
```

---

## Input expectations / GFF format

- The functions expect standard GFF3-like tab-separated lines (9 columns).  
- Attributes column should use `key=value` semicolon-separated pairs (e.g. `ID=gene-1;Name=xyz`).  
- For reference see the GFF3 specification: https://github.com/The-Sequence-Ontology/Specifications/blob/master/gff3.md

---

## Dependencies

- Python >= 3.6 recommended  
- Uses only Python standard libraries: `re`, `os`

---
