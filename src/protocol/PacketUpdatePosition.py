from src.packet.BufferTypes import *
from src.packet.ArrayBuffer import ArrayBuffer

class PacketUpdatePosition:

	def __init__(self, handler, isBinary):
		self.handler = handler
		self.isBinary = isBinary

	def recieve(self, payload):
		self.x = payload.unpackData(int8)[0]
		self.y = payload.unpackData(int8)[0]
		gameserver.notify.setNotifyDebug('Snake %d is going to: x=%d y=%d' % (self.handler.current_snakeId, self.x, self.y))

	def create(self, snake):
		# Update the snake cordinates
		snake.x = self.x
		snake.y = self.y

		# send the update position packet
		buffer = ArrayBuffer()
		buffer.packData(int8, 0) # timestamp
		buffer.packData(int8, 0)
		buffer.packData(int8, ord('g'[0])) # messagetype
		buffer.packData(int8, snake.id)
		buffer.packData(int8, self.x)
		buffer.packData(int8, self.y)
		self.sendData(buffer.getData())
		buffer.clear()

	def sendData(self, message):
		self.handler.sendMessage(message, self.isBinary)