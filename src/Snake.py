
class Snake:

	class body:

		def __init__(self, x, y):
			self.x = x
			self.y = y

	class head:

		def __init__(self, x, y):
			self.x = x
			self.y = y

	def __init__(self, id, x, y, angle, speed, skinId, nameLength, name):
		self.id = id
		self.x = x
		self.y = y
		self.angle = angle
		self.speed = speed
		self.skinId = skinId
		self.nameLength = nameLength
		self.name = name