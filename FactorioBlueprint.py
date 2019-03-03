import zlib
import base64
import json
import enum
import collections

class FactorioBlueprintVersion(enum.Enum):
	Version0 = "0"

class FactorioBaseBlueprint():
	def __init__(self, version, data):
		assert(isinstance(version, FactorioBlueprintVersion))
		self._version = version
		self._data = data

	@property
	def version(self):
		return self._version

	@property
	def data(self):
		return self._data

	@classmethod
	def from_blueprint_str(cls, bp_string):
		versionbyte = bp_string[0]
		version = FactorioBlueprintVersion(versionbyte)
		zlib_data = base64.b64decode(bp_string[1:])
		json_data = zlib.decompress(zlib_data)
		data = json.loads(json_data)
		return cls(version, data)

	def to_blueprint_str(self):
		json_data = json.dumps(self.data).encode("ascii")
		zlib_data = zlib.compress(json_data)
		str_data = str(self.version.value) + base64.b64encode(zlib_data).decode("ascii")
		return str_data

	@classmethod
	def load_file(cls, filename):
		with open(filename) as f:
			return cls.from_blueprint_str(f.read())

	def write_file(self, filename):
		with open(filename, "w") as f:
			f.write(self.to_blueprint_str())


class FactorioBlueprint(FactorioBaseBlueprint):
	def __init__(self, version, data):
		FactorioBaseBlueprint.__init__(self, version, data)
		assert("blueprint" in self.data)

	@property
	def label(self):
		return self.data["blueprint"].get("label")

	@property
	def entities(self):
		return iter(self.data["blueprint"]["entities"])

	def dump_info(self):
		print(self.data["blueprint"]["label"])
		ctr = collections.Counter(entity["name"] for entity in self.entities)
		for (name, value) in ctr.most_common():
			print("%4d x %s" % (value, name))


class FactorioBlueprintBook(FactorioBaseBlueprint):
	def __init__(self, version, data):
		FactorioBaseBlueprint.__init__(self, version, data)
		assert("blueprint_book" in self.data)

	@classmethod
	def create(cls, blueprints):
		assert(all(isinstance(blueprint, FactorioBlueprint) for blueprint in blueprints))
		assert(len(blueprints) > 0)
		data = {
			"blueprint_book": {
				"item":				"blueprint-book",
				"active_index":		0,
				"version":			max(blueprint.data["blueprint"]["version"] for blueprint in blueprints),
				"blueprints":		list(blueprint.data for blueprint in blueprints),
			}
		}
		return cls(version = FactorioBlueprintVersion.Version0, data = data)

	def __iter__(self):
		return (FactorioBlueprint(version = self.version, data = bp_data) for bp_data in self.data["blueprint_book"]["blueprints"])
