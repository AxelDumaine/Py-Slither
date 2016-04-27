from src.packet.BufferTypes import *
from src.packet.ArrayBuffer import ArrayBuffer
import threading

class PacketPong:

	def __init__(self, handler, isBinary):
		self.handler = handler
		self.isBinary = isBinary
		self.thread = None

	def recieve(self, payload):
		buffer = ArrayBuffer()
		buffer.setData(payload)
		self.pingValue = buffer.unpackData(int8)[0]
		buffer.clear()

	def create(self):
		if self.thread != None:
			self.thread.close()

		# lets send pong every one and a half second.
		buffer = ArrayBuffer()
		buffer.packData(int8, 0) # timestamp
		buffer.packData(int8, 0)
		buffer.packData(int8, ord('p'[0])) # messagetype
		self.sendData(buffer.getData())
		# were done, lets continue the thread
		self.startLoop()

	def startLoop(self):
		self.thread = threading.Timer(1.5, self.create).start()

	def sendData(self, message):
		self.handler.sendMessage(message, self.isBinary)