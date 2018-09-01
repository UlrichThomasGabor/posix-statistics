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

def getHeaderName(basedefs, functionname, includesonpage):
	#print(functionname)
	foundkey = None
	# Different syntax than rest, so special if.
	if functionname in ["pthread_cleanup_pop", "pthread_cleanup_push"]:
		foundkey = "pthread.h"
	for key, value in basedefs.items():
		#print(repr(value))
		if re.search(r"\b" + functionname + "\s*\(", value):
			if foundkey == None:
				#print("Found", key, includesonpage)
				if len(includesonpage) == 0 or key in includesonpage:
					foundkey = key
			else:
				if key in includesonpage:
					sys.exit("Oh oh, found functionname \"" + functionname + "\" in " + str(foundkey) + " and again in " + str(key))
	if foundkey == None:
		sys.exit("Found no header file for functionname \"" + functionname + "\" with includes: " + str(includesonpage))
	return foundkey


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Parse all HTML files of POSIX specification and output functions.')
	parser.add_argument("--verbose", action="store_true", default=False)
	args = parser.parse_args()
	makePrintVerbose(args.verbose)

	path_to_standard = "susv4-2018/"
	path_to_standard_basedefs = path_to_standard + "basedefs/"
	path_to_standard_functions = path_to_standard + "functions/"
	htmlfiles_basedefs = [f for f in listdir(path_to_standard_basedefs) if isfile(join(path_to_standard_basedefs, f)) and f.endswith(".h.html")]
	htmlfiles_functions = [f for f in listdir(path_to_standard_functions) if isfile(join(path_to_standard_functions, f)) and f.endswith(".html") and f not in ["toc.html", "V2_chap01.html", "V2_chap02.html", "V2_chap03.html", "contents.html", "V2_title.html"]]
	#print(htmlfiles_functions)
	#print(htmlfiles_basedefs)

	basedefs = {}
	for f in htmlfiles_basedefs:
		headername = f[:-5]
		with open(path_to_standard_basedefs + f, "r") as fh:
			filec = fh.read()
			basedefs[headername.replace("sys_", "sys/").replace("arpa_", "arpa/").replace("net_", "net/")] = filec.split('<div class="box"><em>The following sections are informative.</em></div>')[0]

	nsmap = {"html": "http://www.w3.org/1999/xhtml"}
	for f in htmlfiles_functions:
		printVerbose("Opening: " + str(f))
		with open(path_to_standard_functions + f, "r") as fh:
			filec = fh.read()
			m = re.search("<blockquote>(.+?)</blockquote>", filec, re.DOTALL)
			code = re.search(r"<blockquote class=\"synopsis\">(.+?)</blockquote>", filec, re.DOTALL)
			if m == None:
				sys.exit("Found no function names!")
			if code == None:
				sys.exit("Found no code block!")
			printVerbose(m.group(1))
			functionnames = m.group(1).split("-")[0]
			# Remove variables
			functionnames_list = [x.strip() for x in functionnames.split(",") if x.strip() not in ["environ", "optarg", "opterr", "optind", "optopt", "stderr", "stdin", "stdout", "daylight", "timezone", "tzname", "errno", "signgam"]]
			printVerbose("Matched: " + str(functionnames_list))

			# Remove HTML tags
			codeblock = re.sub(r'<[^<]+?>', '', code.group(1))
			# Convert HTML entities back
			codeblock = html.unescape(codeblock)
			# Convert nbsp's to spaces
			codeblock = codeblock.replace(u'\xa0', u' ')
			# Correct badly formatted include-statements and remove optional specifiers "[XSI]" etc.
			codeblock = re.sub(r'^(?:\s*\[\s*[a-zA-Z ]+\s*\])\s*#include\s*<\s*([a-z/_]+\.h)\s*>\s*', r'#include <\1>\n', codeblock, flags=re.DOTALL|re.MULTILINE)
			printVerbose(codeblock)
			printVerbose(repr(codeblock))
			includes = re.findall(r'^ *#include <([a-z/_]+\.h)>$', codeblock, flags=re.DOTALL|re.MULTILINE)
			printVerbose(includes)
			signatures = re.findall(r"^(?:\s*\[\s*[a-zA-Z ]+\s*\])?\s*[a-zA-Z0-9_\(\)/*\\. ]+\([a-zA-Z0-9_\(\)/*\\. \t\n\r,\-\[\]]*\);?", codeblock, flags=re.DOTALL|re.MULTILINE)
			# Remove special functions from list.
			for special_function in ["FD_CLR", "FD_ISSET", "FD_SET", "FD_ZERO"]:
				signatures = [signature for signature in signatures if not special_function in signature]
			printVerbose(signatures)
			# Check consistency between found signatures on page and listed function names in first paragraph on the same page.
			if len(signatures) != len(functionnames_list):
				print("Numbers of found functions do not match!", len(signatures), "vs", len(functionnames_list))
				sys.exit()

			for signature in functionnames_list:
				# Compute the include_field from the includes we found on the page of the function and the listed functions on the page of the include.
				include_field = str(getHeaderName(basedefs, signature, includes))#",".join(includes)
				print(include_field + "\t" + signature + "\t\\b" + signature + "\s*\(")
			#for x in functionnames_list:
			#	print("\\b" + x + "\s*\(")
