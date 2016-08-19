#!/usr/bin/python

import sys
import os
import argparse
import subprocess
import gzip
import math
import random
from collections import defaultdict
import bedtools
import shutil
import os
import numpy
import genomedata



parser = argparse.ArgumentParser()
parser.add_argument("--tracks", required=True, help="List of genomics data sets in genomedata format the format <archive>\t<trackname>\t<name>")
parser.add_argument("--coords", required=True, help="Coordinates on which to compute correlation. A larger region will result in more time and memory usage.")
parser.add_argument("--outdir", required=True, help="Output directory")
args = parser.parse_args()

print "Reading tracks..."
tracks = []
with open(args.tracks) as f:
    for line in f:
        if line[0] == "#": continue
        line = line.split()
        track_dict = {}
        track_dict["archive_path"] = line[0]
        track_dict["trackname"] = line[1]
        track_dict["name"] = line[2]
        tracks.append(track_dict)


print "Reading coordinates..."
coords = []
total_bases = 0
with open(args.coords) as f:
    for line in f:
        if line[0] == "#": continue
        line = line.split()
        coord_dict = {}
        coord_dict["chrom"] = line[0]
        coord_dict["start"] = int(line[1])
        coord_dict["end"] = int(line[2])
        coord_dict["start_index"] = total_bases
        total_bases += coord_dict["end"] - coord_dict["start"]
        coords.append(coord_dict)

print "Reading data..."
data = numpy.empty(shape=(total_bases, len(tracks)), dtype="float32")
for track_index, track_dict in enumerate(tracks):
    print "Starting track", track_dict["archive_path"], track_dict["trackname"], "..."
    with genomedata.Genome(track_dict["archive_path"]) as g:
        archive_track_index = g.tracknames_continuous.index(track_dict["trackname"])
        for coord_index, coord_dict in enumerate(coords):
            coord_data = g[coord_dict["chrom"]][coord_dict["start"]:coord_dict["end"], archive_track_index]
            num_bases = coord_dict["end"] - coord_dict["start"]
            data[coord_dict["start_index"]:coord_dict["start_index"]+num_bases, track_index] = coord_data

print "Computing correlation matrix..."
corr_mat = numpy.corrcoef(data.T) # compute the pearson correlation among assays
corr_mat = numpy.abs(corr_mat)


print "Writing output..."
if not os.path.exists(args.outdir):
    os.makedirs(args.outdir)

outdir = args.outdir
with open("{outdir}/similarity.tab".format(**locals()), "w") as f:
    for t1 in range(len(tracks)):
        for t2 in range(len(tracks)):
            if t2 != 0:
                f.write("\t")
            f.write("{:.3}".format(corr_mat[t1,t2]))
        f.write("\n")

with open("{outdir}/names.txt".format(**locals()), "w") as f:
    for track_dict in tracks:
        f.write("{}\n".format(track_dict["name"]))

