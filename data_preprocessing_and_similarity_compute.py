#!/usr/bin/python

###############################################################
# Data preprocessing and similarity computation
# Please see README.md for more information
###############################################################

import sys
import numpy as np


def DataPreprocessingAndSimilarityMatrixComputation(raw_data_matrix, simType = "Pearson"):
    # raw_data_matrix is a numpy array with dimension N*d,
    # where N is the number of assays and d is the dimension for each assay.
    
    raw_data_matrix = np.arcsinh(raw_data_matrix) # preprocess the data by asinh function
    if simType == "Pearson":
        corr_mat = np.corrcoef(raw_data_matrix) # compute the pearson correlation among assays
    
    return corr_mat


def main(argv):
    
    ########################################################
    # Load in your own genomics data.
    # Here, we use synthetic data for illustration purpose.
    ########################################################
    
    N = 100
    d = 1000
    rawData = np.random.rand(N,d)
    outputCorr = DataPreprocessingAndSimilarityMatrixComputation(rawData, simType="Pearson")
    #print (outputCorr)




if __name__ == "__main__":
    main(sys.argv[1:])
