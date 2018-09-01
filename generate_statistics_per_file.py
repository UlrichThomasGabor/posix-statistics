#!/usr/bin/env python3
import lxml.etree
from os import listdir
from os.path import isfile, join
import re, sys, html
import argparse

def printVerbose(string):
	if printVerbose._verbose:
		print(string)
printVerbose._verbose = False

def makePrintVerbose(verbose):
	printVerbose._verbose = verbose


def slices(s, *args):
	position = 0
	for length in args:
		yield s[position:position + length]
		position += length

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Will aggregate statistics per file')
	parser.add_argument("--posix_function_list", action="store", default="posix_functions")
	parser.add_argument("posix_count")
	parser.add_argument("--verbose", action="store_true", default=False)
	args = parser.parse_args()
	makePrintVerbose(args.verbose)

	posix_functions = {}
	with open(args.posix_function_list) as f:
		for l in f.readlines():
			l = l[:-1].split("\t")
			posix_functions[l[1]] = l

	posix_count = []
	with open(args.posix_count) as f:
		for l in f.readlines():
			l = [x.strip() for x in l.strip().split(" ")]
			posix_count.append(l)
			#print("\t".join(l))

	combined = []
	for l in posix_count:
		output = l
		output.append(posix_functions[l[1]][0])
		combined.append(output)

	files = sorted(set([x[0] for d, x in posix_functions.items()]))
	per_file = {}
	for f in files:
		per_file[f] = 0

	for l in combined:
		per_file[l[2]] += int(l[0])

	print("\n".join([str(key)+"\t"+str(value) for key, value in per_file.items()]))
