from src.packet.BufferTypes import *
from src.packet.ArrayBuffer import ArrayBuffer

class PacketInitial:

	def __init__(self, handler, isBinary):
		self.handler = handler
		self.isBinary = isBinary

	def recieve(self, payload):
		buffer = ArrayBuffer()
		buffer.setData(payload)
		self.firstId = buffer.unpackData(int8)
		self.secondId = buffer.unpackData(int8)
		self.skinId = buffer.unpackData(int8)
		self.username = str(buffer.getData()[len(self.firstId)+len(self.secondId)+len(self.skinId)-3:])
		# TODO!!: if the player did not set a username, generate one for them.
		buffer.clear()

	def create(self):
		buffer = ArrayBuffer()
		buffer.packData(int8, 0) # timestamp
		buffer.packData(int8, 0)
		buffer.packData(int8, ord('a'[0])) # messagetype
		buffer.packData(int24, 21600)
		buffer.packData(int16, 411)
		buffer.packData(int16, 480)
		buffer.packData(int16, 130)
		buffer.packData(int8, 4.8)
		buffer.packData(int16, 4.25)
		buffer.packData(int16, 0.5)
		buffer.packData(int16, 12)
		buffer.packData(int16, 0.033)
		buffer.packData(int16, 0.28)
		buffer.packData(int16, 0.433)
		buffer.packData(int8, 6) # protocol version?
		self.sendData(buffer.getData())
		buffer.clear()

	def sendData(self, message):
		self.handler.sendMessage(message, self.isBinary)