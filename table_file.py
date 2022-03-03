class TableFile:
	def __init__(self, path, attributes):
		self.path = path
		self.attributes = attributes
		try:
			file = open(self.path, 'rb')
			self.count = int.from_bytes(file.read(4), byteorder='big', signed=False)
			self.data = []
			for y in range(0, self.count, 1):
				obj = {}
				for attribute in self.attributes.attributes:
					obj[attribute['name']] = self.attrib_read(file, attribute['name'])
				self.data.append(obj)
			file.close()
		except FileNotFoundError:
			self.count = 0
			self.data = []
			file = open(path, 'wb')
			file.write(self.count.to_bytes(4, byteorder='big', signed=False))
			file.close()

	def row_get(self, index):
		return self.data[index]

	def attrib_get(self, index, name):
		return self.data[index][name]

	def row_append(self, data):
		file = open(self.path, 'ab')
		self.data.append(data)
		for attrib in self.attributes.attributes:
			name = attrib['name']
			self.attrib_write(file, name, data[name])
		file.close()
		self.count = self.count + 1
		self.count_write(self.count)

	def row_write(self, index, data):
		file = open(self.path, 'wb')
		for attrib in self.attributes.attributes:
			name = attrib['name']
			self.data[index][name] = data[name]
			self.attrib_offset(file, attrib, index)
			self.attrib_write(file, index, name, data[name])
		file.close()

	def attrib_write(self, file, name, data):
		attribute = self.attributes.get_by_name(name)
		if attribute['type'] == ATTRIBUTE_TYPE_STRING:
			file.write(data.encode())
		elif attribute['type'] == ATTRIBUTE_TYPE_INT:
			four_bytes = data.to_bytes(4, byteorder='big', signed=False)
			file.write(four_bytes)

	def attrib_read(self, file, name):
		attribute = self.attributes.get_by_name(name)
		if attribute['type'] == ATTRIBUTE_TYPE_STRING:
			return file.read(attribute['size']).decode()
		elif attribute['type'] == ATTRIBUTE_TYPE_INT:
			return int.from_bytes(file.read(4), byteorder='big', signed=False)

	def count_write(self, count):
		file = open(self.path, 'r+b')
		file.write(count.to_bytes(4, byteorder='big', signed=False))

	def attrib_offset(self, file, attribute, index):
		file.seek(attribute['offset'] + self.attributes.stride * index + 4, 0)

ATTRIBUTE_TYPE_STRING = 0
ATTRIBUTE_TYPE_INT = 1

class FileAttributes:
	def __init__(self):
		self.attribute_indices = {}
		self.attributes = []
		self.stride = 0

	def insert(self, name, _type, size):
		self.attribute_indices[name] = len(self.attributes)
		self.attributes.append(
			{
				'name': name,
				'size': size,
				'type': _type,
				'offset': self.stride
			}
		)
		self.stride += size

	def get_by_name(self, name):
		return self.attributes[self.attribute_indices[name]]

	def get_by_index(self, index):
		return self.attributes[index]
