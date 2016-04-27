from src.packet.BufferTypes import *
from src.packet.ArrayBuffer import ArrayBuffer
from src.Snake import Snake
import math

class PacketCreateSnake:

	def __init__(self, handler, isBinary):
		self.handler = handler
		self.isBinary = isBinary

	def recieve(self, payload):
		pass

	def create(self, values=[]):
		snake = Snake(values[0], values[1], values[2], values[3], values[4], values[5], values[6], values[7])
		snake.body = Snake.body(0, 0)
		snake.head = Snake.head(0, 0)
		gameserver.generatedSnakes.append(snake)

		# send generate snake packet to the client.
		buffer = ArrayBuffer()
		buffer.packData(int8, 0) # timestamp
		buffer.packData(int8, 0)
		buffer.packData(int8, ord('s'[0])) # messagetype
		buffer.packData(int16, snake.id) # self.snakeId
		buffer.packData(int24, 5 * math.pi / 16777215)
		buffer.packData(int8, 0) # unused?
		buffer.packData(int24, 360 * math.pi / 16777215 )
		buffer.packData(int16, snake.speed)
		buffer.packData(int24, 5 / 16777215)
		buffer.packData(int8, snake.skinId)
		buffer.packData(int24, snake.body.x)
		buffer.packData(int24, snake.body.y)
		buffer.packData(int8, len(snake.name.encode('utf-8')))
		for char in snake.name:
			buffer.packData(string, char.encode('utf-8'))
		buffer.packData(int24, snake.head.x)
		buffer.packData(int24, snake.head.y)
		buffer.packData(int8, snake.body.x)
		buffer.packData(int8, snake.body.y)
		self.sendData(buffer.getData())
		buffer.clear()

	def sendData(self, message):
		self.handler.sendMessage(message, self.isBinary)