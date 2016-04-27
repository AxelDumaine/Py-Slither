from src.packet.BufferTypes import *
from src.packet.ArrayBuffer import ArrayBuffer
import threading, random

class PacketCreateFood:

	def __init__(self, handler, isBinary):
		self.handler = handler
		self.isBinary = isBinary
		self.thread = None

	def recieve(self, payload):
		pass

	def create(self):
		if self.thread != None:
			self.thread.close()

		buffer = ArrayBuffer()
		buffer.packData(int8, 0) # timestamp
		buffer.packData(int8, 0)
		buffer.packData(int8, ord('F'[0])) # messagetype
		color = random.randint(0, 10)
		buffer.packData(int8, color)
		x = random.randint(0, 3000)
		y = random.randint(0, 3000)
		buffer.packData(int16, x)
		buffer.packData(int16, y)
		buffer.packData(int8, color)
		self.sendData(buffer.getData())
		# were done, lets continue the thread
		self.startLoop()

	def startLoop(self):
		self.thread = threading.Timer(1.0, self.create).start()

	def sendData(self, message):
		self.handler.sendMessage(message, self.isBinary)