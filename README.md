Submodular-Selection-of-Assays (SSA)
==

Please see the following reference for more details:
Kai Wei * , Maxwell W. Libbrecht * , Jeffrey A Bilmes, William S. Noble. "Evaluation and selection of panels of genomics assays." Submitted.

Get the most recent version on [github](https://github.com/kaiwei123/Submodular-Selection-of-Assays).

* Author: Kai Wei
* Email: kaiwei@uw.edu
* Melodi Lab, University of Washington, Seattle

Arguments
--

* List of assay names (--names):
A text file with N lines, with each line being an assay name.  
An example of the assay name file can be found in the file `assay_names_all.txt`.

* Similarity matrix (--sim):
A text file containing a symmetric square matrix of size N by N, with each entry being non-negative. The file should have N lines, with each line corresponding to a row of the matrix, and with columns delimited by spaces. 
An example similarity matrix can be found in the file `similarity_matrix_all.txt`. 

* Output file name (--output):
The path for the file where the selected list of items is to stored. 

Sample command line
--

    python greedy_selection_facility_location.py --names=assay_names_all.txt --sim=similarity_matrix_all.txt --output=ordered_assay_list.txt


