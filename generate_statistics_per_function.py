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
	parser = argparse.ArgumentParser(description='Run campaign')
	parser.add_argument("--posix_function_list", action="store", default="posix_functions")
	parser.add_argument("posix_count")
	parser.add_argument("--verbose", action="store_true", default=False)
	parser.add_argument("--topN", default=500, type=int, help="list only N entries counted most often")
	args = parser.parse_args()
	makePrintVerbose(args.verbose)

	posix_functions = {}
	with open(args.posix_function_list) as f:
		for l in f.readlines():
			l = l[:-1].split("\t")
			posix_functions[l[1]] = l
	# print(posix_functions)

	posix_count = []
	with open(args.posix_count) as f:
		for l in f.readlines():
			l = [x.strip() for x in l.strip().split(" ")]
			posix_count.append(l)
			#print("\t".join(l))

	# Compute min. count based on topN
	if len(posix_count) >= args.topN:
		mincount = int(sorted(posix_count, key=lambda a: int(a[0]))[-args.topN-1][0])
	else:
		mincount = -1

	for l in posix_count:
		if int(l[0]) > mincount:
			output = l
			output.append(posix_functions[l[1]][0])
			print("\t".join(output))
