# Submodular-Selection-of-Assays

The input arguments to the python script include the following:  

-- Similarity matrix:
An example of the similarity matrix can be found in the file "Generic_Aggregation_Sim_Matrix.txt". 
The input similarity matrix should be a symmetric square matrix of size N*N with each entry being non-negative. The matrix is stored in an ASCII format file. The file has N lines, with each line corresponding to a row of the matrix. All entries in the file are delimited with a space. 

-- n: 
Total number of items in the data set. 

-- k:
Number of items to select. 

-- Reference name list:
An example of the reference name list can be found in the file "Assay_list.txt".
The reference name list should be stored in an ASCII format file. The file has N lines with each line being the referenece name for the corresponding item.  

-- Output file name:
The path for the file where the selected list of items is to stored. 

A sample command for running the code is

python greedy_selection_facility_location.py -i Generic_Aggregation_Sim_Matrix.txt -n `less Assay_list.txt | wc -l` -k 10 -o output_selected_list -r Assay_list.txt


