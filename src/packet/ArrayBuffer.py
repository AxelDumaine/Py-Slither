import struct

class ArrayBuffer:

	def __init__(self):
		self.data = b''

	def setData(self, data):
		self.data = b'%s' % data

	def getData(self):
		return self.data

	def packData(self, type, value):
		# Make sure the floats are integers.
		try:
			packed = type.pack(int(value))
		except:
			packed = type.pack(value)

		self.data = self.data + packed

	def unpackData(self, type):
		unpacked = type.unpack_from(self.data)
		self.data = self.data[len(unpacked):]
		return unpacked

	def clear(self):
		self.data = b''