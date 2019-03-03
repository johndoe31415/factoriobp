#!/usr/bin/python3
#
#
import os
import sys
import contextlib
from FactorioBlueprint import FactorioBlueprint, FactorioBlueprintBook

book_filename = sys.argv[1]
output_dir = sys.argv[2]

with contextlib.suppress(FileExistsError):
	os.makedirs(output_dir)
book = FactorioBlueprintBook.load_file(book_filename)
for (bpno, blueprint) in enumerate(book, 1):
	if blueprint.label is None:
		filename = "%s/%02d.txt" % (output_dir, bpno)
	else:
		label = blueprint.label.replace(" ", "_")
		filename = "%s/%02d_%s.txt" % (output_dir, bpno, label)
	blueprint.write_file(filename)
