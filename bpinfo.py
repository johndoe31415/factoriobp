#!/usr/bin/python3
#
#
import os
import sys

from FactorioBlueprint import FactorioBlueprint

bp = FactorioBlueprint.from_file(sys.argv[1])
bp.dump_info()
