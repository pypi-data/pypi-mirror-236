## MarkerCount update
- Sept 01, 2022: Added HiCAT, an updated version of MarkerCount.
- Dec. 06, 2021: Now, MarkerCount can be used in R. Please see the instruction below.
- June 27, 2021: Slight modification was made to improve the identification performance.


## HiCAT

![PyPI Version](https://img.shields.io/pypi/v/MarkerCount.svg)  ![PyPI Downloads](https://img.shields.io/pypi/dm/MarkerCount.svg)  

- HiCAT is a marker-based, hierarchical cell-type annotation tool for single-cell RNA-seq data.
- It was developed using python3, but also run in R as well.
- HiCAT works in marker-based mode utilizing only the existing lists of markers.
- Github page: https://github.com/combio-dku/HiCAT
- Please refer to "Hierarchical cell-type identifier accurately distinguishes immune-cell subtypes enabling precise profiling of tissue microenvironment with single-cell RNA-sequencing", Briefings in Bioinformatics, available at https://doi.org/10.1093/bib/bbad006,  https://doi.org/10.1101/2022.07.27.501701

### Installation using pip and importing HiCAT in Python

HiCAT can be installed using pip command. With python3 installed in your system, simply use the follwing command in a terminal.

`pip install MarkerCount`

Once it is installed using pip, you can import two functions using the following python command.

`from MarkerCount.hicat import HiCAT, show_summary`

where `show_summary` is used to check the annotation results.

Please check HiCAT github page https://github.com/combio-dku/HiCAT for its usage and example jupyter notebook. 

### HiCAT marker file format

Marker file must be a tap-separated-value file (.tsv) with 5 columns, "cell_type_major", "cell_type_minor", "cell_type_subset", "exp" and "markers".
- The first three columns define the 3-level taxonomy tree to be used for hierarchical identification.
- "exp" is type of marker, which can be "pos", "neg", or "sec".
- "markers" is a list of gene symbols separated by comma.
- The markers in "cell_markers_rndsystems_rev.tsv", were reproduced from [R&D systems](https://www.rndsystems.com/resources/cell-markers)

If you want to use your own markers, please refer to the [tips for prepareing markers db](https://github.com/combio-dku/HiCAT/blob/main/PreparingMarkersDB.md).

## MarkerCount and MarkerCount-Ref (Previous version)

- MarkerCount is a python3 cell-type identification toolkit for single-cell RNA-Seq experiments.
- MarkerCount works both in reference and marker-based mode, where the latter utilizes only the existing lists of markers, while the former required pre-annotated dataset to train the model. 
- Please refer to the preprint manuscript "MarkerCount: A stable, count-based cell type identifier for single cell RNA-Seq experiments" available at https://www.researchsquare.com/article/rs-418249/v2 DOI: https://doi.org/10.21203/rs.3.rs-418249/v2 

### Installation and importing MarkerCount

All the functions to implement MarkerCount are defined in the python3 script, `marker_count.py`, where the two key functions are 

1. `MarkerCount()`: marker-based cell-type identifier
1. `MarkerCount_Ref()`: reference-based cell-type identifier

One can import the function by adding a line in your script, i.e., `from marker_count import MarkerCount_Ref, MarkerCount`

Please check MarkerCount github page https://github.com/combio-dku/MarkerCount for its usage and example jupyter notebook. 

## Contact
Send email to syoon@dku.edu for any inquiry on the usages.

