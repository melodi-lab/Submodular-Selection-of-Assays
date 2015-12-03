#!/usr/bin/python

###############################################################
# Submodular Selection of Assays (SSA)
# Please see README.md for more information
###############################################################

import sys, getopt
import heapq
import argparse

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

def facility_location_gain(sim_matrix, new_item, precompute, N_ground):
    func_val = 0;
    for index in range(0, N_ground, 1):
        if sim_matrix[new_item][index] > precompute[index]:
            func_val = func_val + sim_matrix[new_item][index];
        else:
            func_val = func_val + precompute[index];
    return func_val

def facility_location_evaluate(sim_matrix, chosen, N_ground):
    if len(chosen) == 0: return 0
    func_val = 0;
    for eval_index in range(0, N_ground):
        func_val += max([sim_matrix[eval_index][chosen_index] for chosen_index in chosen])
    return func_val

def main(argv):

        ########################################
        # Read command-line arguments
        ########################################

        parser = argparse.ArgumentParser(description="This script implements the Submodular Selection of Assays (SSA) method for selecting a panel of genomics assays.  Takes as input a list of assay names and a matrix of assay-assay similarity values.  Outputs an ordered list of assay types, where the top K items in the list is the chosen panel of size K.")
        parser.add_argument("--sim", required=True, help="Path to symmetric matrix of nonnegative similarity values, with columns delimited by spaces and rows delimited by newlines. The numbers of rows, columns and assay names must be identical.")
        parser.add_argument("--names", required=True, help="Path to newline-delimited file specifying the assay type names.")
        parser.add_argument("--output", required=True, help="Output path")
        args = parser.parse_args()

        ########################################
        # Read assay type name file
        ########################################

        try:
            f = open(args.names, 'r')
        except IOError:
            raise Exception('ERROR: Could not open the assay names file: {0}'.format(args.names))
            sys.exit(1)
        reference_list = f.readlines()
        N_ground = len(reference_list)
        f.close()

        ########################################
        # Read similarity matrix
        ########################################
        try:
            f = open(args.sim, 'r')
        except IOError:
            raise Exception('ERROR: Could not open the file: {0}'.format(args.sim))
            sys.exit(1)

        text_lines = f.readlines()
        f.close()
        sim_matrix = []
        for line in text_lines:
            line.strip('\n');
            vec = line.split()
            vec = map(float, vec)
            if (all(i >= 0 for i in vec)) == False:
                raise Exception("ERROR: The input similarity matrix contains negative values")
                sys.exit(1)
            if len(vec) <> N_ground:
                raise Exception("ERROR: The dimension of the similarity matrix does not agree with the input ground set size")
                sys.exit(1)
            sim_matrix.append(vec)

        if len(sim_matrix) <> N_ground:
            raise Exception("ERROR: The dimension of the similarity matrix does not agree with the input ground set size")
            sys.exit(1)

        # check the symmetry of the data matrix
        for idx in range(0, N_ground, 1):
            for jdx in range(idx, N_ground, 1):
                if sim_matrix[idx][jdx] != sim_matrix[jdx][idx]:
                    raise Exception("ERROR: the input data matrix is not symmetric")
                    sys.exit(1)

        ########################################
        # Select assay type order using the accelerated greedy algorithm
        ########################################

        assay_type_order = [];
        precompute = [0] * N_ground

        index = 1;
        priority_q = PriorityQueue()
        prev_func_val = 0;
        # initialize the priority queue
        for item in range(0,N_ground,1):
            func_val = facility_location_gain(sim_matrix, item, precompute, N_ground)
            data_item = (item, func_val)
            priority_q.push(data_item, func_val)

        while (not priority_q.isempty()):
            max_val = 0;
            data_item = priority_q.pop()
            new_func_val = facility_location_gain(sim_matrix, data_item[0], precompute, N_ground)
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
                assay_type_order.append(data_item[0])
                prev_func_val = new_func_val
                assert (abs(new_func_val - facility_location_evaluate(sim_matrix, assay_type_order, N_ground)) < 1e-3)
                print "Selecting item ", reference_list[data_item[0]].strip('\n'),'. After update, the facility location objective value is ', new_func_val

                # update the precompute
                for index in range(0, N_ground, 1):
                    if sim_matrix[index][data_item[0]] > precompute[index]:
                        precompute[index] = sim_matrix[index][data_item[0]]

        ########################################
        # Write ordered assay types to file
        ########################################

        try:
            f = open(args.output, 'w')
        except IOError:
            raise Exception('ERROR: Could not open {0} for writing'.format(args.output))
            sys.exit(1)

        for item in assay_type_order:
            f.write(str(reference_list[item].strip('\n')) + '\n')
        f.close()

if __name__ == "__main__":
    main(sys.argv[1:])
