#!/usr/bin/python

###############################################################
# This script implements the Naive/Accelerated greedy algorithm
# for solving the cardinality constrained facility location function 
# maximization. 

# Author: Kai Wei
# Email: kaiwei@uw.edu
# Melodi Lab, University of Washington, Seattle
###############################################################


import sys, getopt
import warnings
warnings.simplefilter("ignore", DeprecationWarning)
from sets import Set
import heapq


class PriorityQueue:
    def __init__(self):
        self._queue = []
        self._index = 0

    def push(self, item, priority):
        heapq.heappush(self._queue, (-priority, self._index, item))
        self._index += 1

    def pop(self):
        self._index -= 1
        return heapq.heappop(self._queue)[-1]
    def isempty(self):
        if self._index == 0:
            return True
        else:
            return False

def main(argv):
        similarity_graph = ''
        reference_file = ''
        output_list = ''
        K_budget = 0;
        N_ground = 0;
        Data_Mat = [];
        #Alg_type = 'NaiveGreedy'
        Alg_type = 'AccGreedy'
# Process the input arguments 
        try:
            opts, args = getopt.getopt(argv,"hi:n:k:o:r:")
        except getopt.GetoptError:
            print 'greedy_selection_facility_location.py -i <similarity graph> -r <reference name for the similarity graph> -n <total number of items> -k <number of items to select> -o <selected list>'
            sys.exit(2)
        for opt, arg in opts:
            if opt == '-h':
                print 'greedy_selection_facility_location.py -i <similarity graph> -r <reference name for the similarity graph> -n <total number of items> -k <number of items to select> -o <selected list>'
                sys.exit()
            elif opt in ("-i"):
                similarity_graph = arg
            elif opt in ("-o"):
                output_list = arg
            elif opt in ("-k"):
                K_budget = arg
            elif opt in ("-n"):
                N_ground = arg
            elif opt in ("-r"):
                reference_file = arg
        if (K_budget == 0) | (N_ground == 0) | (output_list == '') | (similarity_graph == ''):
            print 'ERROR: Not enough input argument'
            print 'greedy_selection_facility_location.py -i <similarity graph> -r <reference name for the similarity graph> -n <total number of items> -k <number of items to select> -o <selected list>'
            sys.exit(1)

        #print 'Input similarity graph is ', similarity_graph
        #print 'Total number of items = ', N_ground
        #print 'Number of items to select = ', K_budget
        #print 'Output file is ', output_list
        N_ground = int(N_ground)
        K_budget = int(K_budget)
        if reference_file == '':
            reference_list = range(0,N_ground,1)
        else:
            try:
                f = open(reference_file, 'r')
            except IOError:
                print 'ERROR: Could not open the reference file: ', reference_file
                print 'Please double check the file path'
                sys.exit(1)
            reference_list = f.readlines()
            if len(reference_list) != N_ground:
                print 'ERROR: the number of lines in the reference file does not match the total number of items in the similarity matrix'
                sys.exit(1)
            f.close()

        if K_budget > N_ground:
            print "ERROR: selection budget cannot be greater than the total number of items"
            sys.exit(1)

# read the similarity graph, and make sure that the data is in right format
        try:
            f = open(similarity_graph, 'r')
        except IOError:
            print 'ERROR: Could not open the file:', similarity_graph 
            print 'Please double check the file path'
            sys.exit(1)

        text_lines = f.readlines()
        f.close()
        for line in text_lines:
            line.strip('\n');
            vec = line.split()
            vec = map(float, vec)
            #print vec
            if (all(i >= 0 for i in vec)) == False:
                print "ERROR: Some entry of the input data matrix is negative"
                sys.exit(1)
            if len(vec) <> N_ground:
                print "ERROR: Dimension of the similarity matrix does not agree with the input ground set size"
                sys.exit(1)
            Data_Mat.append(vec)

        if len(Data_Mat) <> N_ground:
            print "ERROR: Dimension of the similarity matrix does not agree with the input ground set size"
            sys.exit(1)

# check the symmetry of the data matrix
        for idx in range(0, N_ground, 1):
            for jdx in range(idx, N_ground, 1):
                if Data_Mat[idx][jdx] != Data_Mat[jdx][idx]:
                    print 'ERROR: the input data matrix is not symmetric: it requires the similarity matrix to be symmetric, and with each entry being non-negative'
                    sys.exit(1)

        Selected_list = [];
        Remain_set = Set(range(0, N_ground, 1));
        precompute = [0] * N_ground

# Naive greedy algorithm          
        if Alg_type == 'NaiveGreedy':
            while len(Selected_list) < K_budget:
                max_val = 0;
                select_item = 0;
                for item in Remain_set:
                    func_val = facility_location_gain(Data_Mat, item, precompute, N_ground)
                    if func_val > max_val:
                        select_item = item
                        max_val = func_val
                Selected_list.append(select_item)
                #print len(Selected_list)
                print "Selecting item ", select_item, ', after update, the value is ', max_val
                Remain_set.remove(select_item)

# update the precompute
                for index in range(0, N_ground, 1):
                    if Data_Mat[index][select_item] > precompute[index]:
                        precompute[index] = Data_Mat[index][select_item]

# Accelerated greedy algorithm
        if Alg_type == 'AccGreedy':
            index = 1;
            priority_q = PriorityQueue()
            prev_func_val = 0;
            # initialize the priority queue
            for item in range(0,N_ground,1):
                func_val = facility_location_gain(Data_Mat, item, precompute, N_ground)
                data_item = (item, func_val)
                priority_q.push(data_item, func_val)

            while (len(Selected_list) < K_budget) & (priority_q.isempty() == False):
                max_val = 0;
                data_item = priority_q.pop()
                new_func_val = facility_location_gain(Data_Mat, data_item[0], precompute, N_ground)
                new_func_gain = new_func_val - prev_func_val
                if priority_q.isempty() == True:
                    second_top_item = (-1, 0) # dummy 
                else:
                    second_top_item = priority_q.pop()
                    priority_q.push(second_top_item, second_top_item[1])

                if new_func_gain < second_top_item[1]:
                    new_data_item = (data_item[0], new_func_gain)
                    priority_q.push(new_data_item, new_func_gain)
                else:
                    Selected_list.append(data_item[0])
                    prev_func_val = new_func_val
                    if reference_file == '':
                        print "Selecting item ", data_item[0], ', after update, the value is ', new_func_val
                    else:
                        print "Selecting item ", reference_list[data_item[0]].strip('\n'),', after update, the value is ', new_func_val

                    # update the precompute
                    for index in range(0, N_ground, 1):
                        if Data_Mat[index][data_item[0]] > precompute[index]:
                            precompute[index] = Data_Mat[index][data_item[0]]

                    


                    
# print the order of selected items
        try:
            f = open(output_list, 'w')
        except IOError:
            print 'ERROR: Could not open ', output_list, ' for writing'
            print 'Please double check the path'
            sys.exit(1)
            
        f.write('Notice that the indices start from 0\n')
        for item in Selected_list:
            f.write(str(reference_list[item].strip('\n')) + '\n')
        f.close()
        #print Selected_list

def facility_location_gain(Data_Mat, new_item, precompute, N_ground):
    func_val = 0;
    for index in range(0, N_ground, 1):
        if Data_Mat[new_item][index] > precompute[index]:
            func_val = func_val + Data_Mat[new_item][index];
        else:
            func_val = func_val + precompute[index];
    return func_val

if __name__ == "__main__":
    main(sys.argv[1:])
