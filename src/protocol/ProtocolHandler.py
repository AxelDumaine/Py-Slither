from autobahn.asyncio.websocket import WebSocketServerProtocol
from src.protocol.Connection import Connection
from src.packet.BufferTypes import *
from src.packet.ArrayBuffer import ArrayBuffer
import struct, re, time, random, math

class ProtocolHandler(WebSocketServerProtocol):
	current_connection = None
	current_cellId = 0

	def onConnect(self, request):
		self.current_connection = Connection(request)
		gameserver.activeConnections.append(self.current_connection)

	def onOpen(self):
		pass

	def onMessage(self, payload, isBinary):
		if self.current_connection not in gameserver.activeConnections:
			# This shouldn't ever happen but if for some unknown reason:
			# Something happened, because we don't know about this connection!
			return

		buffer = ArrayBuffer()
		buffer.setData(payload)
		data = buffer.getData()

		if data.find(b'=' or b'==') != -1:
			for char in data:
				buffer.packData(string, b'' + bytearray(char))

		self.sendMessage(buffer.getData(), isBinary)
		buffer.clear()

		buffer = ArrayBuffer()
		buffer.packData(uint8, 16)
		buffer.packData(uint16, 0)
		buffer.packData(uint32, 1)
		buffer.packData(uint32, 0)
		buffer.packData(uint32, 0)
		buffer.packData(uint16, 15)
		buffer.packData(uint8, 1)
		buffer.packData(uint8, 1)
		buffer.packData(uint8, 1)
		buffer.packData(uint8, 0) # flags
		buffer.packData(uint32, 0) # skipbytes
		buffer.packData(uint8, 0)
		buffer.packData(uint16, 0)
		buffer.packData(uint32, 0)
		buffer.packData(uint32, 0)
		self.sendMessage(buffer.getData(), isBinary)

		print (payload)

	def getTimestamp(self):
		pass

	def setLastSent(self, timestamp):
		gameserver.timestamp = timestamp

	def getLastSent(self):
		return gameserver.timestamp

	def allocateNewSnakeId(self):
		return random.randint(0, gameserver.maxCellIds)

	def getRandomSpawnPoint(self):
		x = random.randint(0, 70000)
		y = random.randint(0, 70000)
		return (x, y)

	def onClose(self, wasClean, code, reason):
		gameserver.activeConnections.remove(self.current_connection)
		self.current_connection = None

		# reset the clients snake to None
		for cell in gameserver.generatedCells:
			if cell.id == self.current_cellId:
				gameserver.generatedCells.remove(cell)
