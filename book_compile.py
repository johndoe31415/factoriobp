#!/usr/bin/python3
#
#
import os
import sys
import contextlib
from FactorioBlueprint import FactorioBlueprint, FactorioBlueprintBook

input_dir = sys.argv[1]
book_filename = sys.argv[2]

blueprints = [ ]
for filename in sorted(os.listdir(input_dir)):
	blueprint = FactorioBlueprint.load_file(input_dir + "/" + filename)
	blueprints.append(blueprint)

book = FactorioBlueprintBook.create(blueprints)
book.write_file(book_filename)
