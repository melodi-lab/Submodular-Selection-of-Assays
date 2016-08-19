Submodular-Selection-of-Assays (SSA)
==

Please see the following reference for more details:
Kai Wei * , Maxwell W. Libbrecht * , Jeffrey A Bilmes, William S. Noble. "Evaluation and selection of panels of genomics assays." Submitted.

Get the most recent version on [github](https://github.com/melodi-lab/Submodular-Selection-of-Assays).

* Author: Kai Wei, Maxwell Libbrecht
* Email: kaiwei@uw.edu, maxwl@cs.washington.edu
* Melodi Lab, University of Washington, Seattle

greedy_selection_facility_location.py
--

### Arguments

* List of assay names (--names):
A text file with N lines, with each line being an assay name.  
An example of the assay name file can be found in the file `assay_names_<type>.txt` where the type is one of "histonemods", "tfs" (transcription factors) or "all".

* Similarity matrix (--sim):
A text file containing a symmetric square matrix of size N by N, with each entry being non-negative. The file should have N lines, with each line corresponding to a row of the matrix, and with columns delimited by spaces. 
An example similarity matrix can be found in the file `similarity_matrix_<type>.txt`.

* Assay types to select from (--selectFrom) (optional):
A subset of the assay types that should be selected from.
The file should be a newline-delimited list of names, where each name is included in the `--names` file.
If not specified, all assay types are included.

* Output file name (--output):
The path for the file where the selected list of items is to stored. 

### Sample command line

    python greedy_selection_facility_location.py --names=assay_names_all.txt --sim=similarity_matrix_all.txt --output=ordered_assay_list.txt

greedy_selection_facility_location_SSA_past.py
--

### Submodular Assay Selection under past setting (SSA-past)

We provide the source code for running assay selection under the past setting, where the goal is to select from a list of assays already performed on a given cell type. The script is found at `SSA_past/greedy_selection_facility_location_SSA_past.py`.

### Sample command line
    
    cd SSA_past;
    python greedy_selection_facility_location_SSA_past.py --cellType=K562 --output=ordered_assay_list.txt
    
similarity_matrix.py
--

This script computes a similarity matrix over a number of genomics data sets.
The genomics data must be in [genomedata format](https://www.pmgenomics.ca/hoffmanlab/proj/genomedata/).

### Arguments

* List of tracks (--tracks):
A text file with one line per track.
Each row should have three tab-delimited fields:
(1) The path to the genomedata archive that contains this track;
(2) The name of the track within the genomedata archive; and 
(3) The desired name this track should go by in the SSA output.

* Coordinates (--tracks):
A [bed3 file](https://genome.ucsc.edu/FAQ/FAQformat.html#format1) with the coordinates over which the correlation should be computed.
A larger coordinate region results in more accurate correlations, but more time and memory usage.

* Output directory (--outdir):
Directory for the output files.

### Output

The script will put two files in the output directory: `similarity.tab` and `names.txt`. These files can be input into `greedy_selection_facility_location.py` using the `--sim` and `--names` arguments respectively.

### Sample command line

    python similarity_matrix.py --tracks=example_tracks.txt --coords=example_coords.txt --output=out
