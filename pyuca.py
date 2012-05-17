# pyuca - Unicode Collation Algorithm
# Credits : James Tauber http://jtauber.com/
# Modified by Santhosh Thottingal for dumping the table in json formatDigit
# License: GPLv2+
# Date: 2012 May 17


"""
Preliminary implementation of the Unicode Collation Algorithm.


This only implements the simple parts of the algorithm but I have successfully
tested it using the Default Unicode Collation Element Table (DUCET) to collate
Ancient Greek correctly.

Usage example:

	from pyuca import Collator
	c = Collator("allkeys.txt")

	sorted_words = sorted(words, key=c.sort_key)

allkeys.txt (1 MB) is available at

	http://www.unicode.org/Public/UCA/latest/allkeys.txt

but you can always subset this for just the characters you are dealing with.
"""

import json
import os
import sys
class Trie:

	def __init__(self):
		self.root = [None, {}]

	def add(self, key, value):
		curr_node = self.root
		for part in key:
			curr_node = curr_node[1].setdefault(part, [None, {}])
		curr_node[0] = value

	def find_prefix(self, key):
		curr_node = self.root
		remainder = key
		for part in key:
			if part not in curr_node[1]:
				break
			curr_node = curr_node[1][part]
			remainder = remainder[1:]
		return (curr_node[0], remainder)


class Collator:

	def __init__(self, filename,start_range, end_range):

		self.table = Trie()
		self.start = start_range
		self.end = end_range
		self.load(filename,start_range, end_range)

	def load(self, filename, start_range, end_range):
		for line in open(filename):
			if line.startswith("#") or line.startswith("%"):
				continue
			if line.strip() == "":
				continue
			line = line[:line.find("#")] + "\n"
			line = line[:line.find("%")] + "\n"
			line = line.strip()
		
			if line.startswith("@"):
				pass
			else:
				semicolon = line.find(";")
				charList = line[:semicolon].strip().split()
				x = line[semicolon:]
				collElements = []
				integer_points = [int(ch, 16) for ch in charList]
				if not (integer_points[0] >=  self.start and integer_points[0] <= self.end):
					if integer_points[0] >= 1000:
						continue
				while True:
					begin = x.find("[")
					if begin == -1:
						break				
					end = x[begin:].find("]")
					collElement = x[begin:begin+end+1]
					x = x[begin + 1:]
					alt = collElement[1]
					chars = collElement[2:-1].split(".")
					collElements.append((alt,chars))
				#print str(integer_points) + ":" + str(collElements)
				self.table.add(integer_points, collElements)

	def sort_key(self, string):
		
		collation_elements = []

		lookup_key = [ord(ch) for ch in string]
		while lookup_key:
			value, lookup_key = self.table.find_prefix(lookup_key)
			if not value:
				# @@@
				raise Exception
			collation_elements.extend(value)
	
		sort_key = []
		
		for level in range(4):
			if level:
				sort_key.append(0)
			for element in collation_elements:
				#sort_key.append(int(element[1][level], 16))
				sort_key.append(element[1][level])
				
		return tuple(sort_key)

if __name__ == '__main__':
	if len(sys.argv) < 4:
		print "Python DUCET to json format convertor"
		print "Usage: python pyuca.py ducetfile start end"
		print "\tducetfile - This is usually allkeys.txt, can be downloaded from http://www.unicode.org/Public/UCA/latest/allkeys.txt"
		print "\tstart - start of unicode range. In base 10"
		print "\tend - start of unicode range. In base 10"
		print "Example:  python pyuca.py allkeys-6.0.0.txt 3330 3428"
	else:
		ucacollator = Collator(os.path.join(os.path.dirname(__file__), sys.argv[1]), sys.argv[2], sys.argv[3])
		print "trie = "+ json.dumps(ucacollator.table.root, sort_keys=True) + ";"

