import zlib
import base64
import json
import enum
import collections

class FactorioBlueprintVersion(enum.Enum):
	Version0 = "0"

class FactorioBlueprint():
	def __init__(self, version, data):
		assert(isinstance(version, FactorioBlueprintVersion))
		self._version = version
		self._data = data

	@property
	def data(self):
		return self._data

	@property
	def entities(self):
		return iter(self._data["blueprint"]["entities"])

	@classmethod
	def from_blueprint_str(cls, bp_string):
		versionbyte = bp_string[0]
		version = FactorioBlueprintVersion(versionbyte)
		zlib_data = base64.b64decode(bp_string[1:])
		json_data = zlib.decompress(zlib_data)
		data = json.loads(json_data)
		return cls(version, data)

	@classmethod
	def from_file(cls, filename):
		with open(filename) as f:
			return cls.from_blueprint_str(f.read())

	def dump_info(self):
		print(self.data["blueprint"]["label"])
		ctr = collections.Counter(entity["name"] for entity in self.entities)
		for (name, value) in ctr.most_common():
			print("%4d x %s" % (value, name))
