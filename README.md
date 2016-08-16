Submodular-Selection-of-Assays (SSA)
==

Please see the following reference for more details:
Kai Wei * , Maxwell W. Libbrecht * , Jeffrey A Bilmes, William S. Noble. "Evaluation and selection of panels of genomics assays." Submitted.

Get the most recent version on [github](https://github.com/kaiwei123/Submodular-Selection-of-Assays).

* Author: Kai Wei, Maxwell Libbrecht
* Email: kaiwei@uw.edu, maxwl@cs.washington.edu
* Melodi Lab, University of Washington, Seattle

Arguments
--

* List of assay names (--names):
A text file with N lines, with each line being an assay name.  
An example of the assay name file can be found in the file `assay_names_<type>.txt` where the type is one of "histonemods", "tfs" (transcription factors) or "all".

* Similarity matrix (--sim):
A text file containing a symmetric square matrix of size N by N, with each entry being non-negative. The file should have N lines, with each line corresponding to a row of the matrix, and with columns delimited by spaces. 
An example similarity matrix can be found in the file `similarity_matrix_<type>.txt`.

* Output file name (--output):
The path for the file where the selected list of items is to stored. 

Sample command line
--

    python greedy_selection_facility_location.py --names=assay_names_all.txt --sim=similarity_matrix_all.txt --output=ordered_assay_list.txt

Data preprocessing and similarity computation
--

For completeness, we also provide the source code for performing data preprocessing and similarity computation on the genomics assay data. Please refer to `data_preprocessing_and_similarity_compute.py` for details. 

Submodular Assay Selection under past setting (SSA-past)
--

We provide the source code for running assay selection under the past setting, where the goal is to select from a list of assays already performed on a given cell type. The script is found at `SSA_past/greedy_selection_facility_location_SSA_past.py`.

Sample command line
--
    
    cd SSA_past;
    python greedy_selection_facility_location_SSA_past.py --cellType=K562 --output=ordered_assay_list.txt
    
