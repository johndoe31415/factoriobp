#!/usr/bin/python3
#
#
import os
import sys

from FactorioBlueprint import FactorioBlueprint

for filename in sys.argv[1:]:
	bp = FactorioBlueprint.load_file(filename)
	print(filename)
	bp.dump_info()
	print()
