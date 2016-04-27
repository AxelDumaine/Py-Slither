from autobahn.asyncio.websocket import WebSocketServerProtocol
from src.protocol.Connection import Connection
from src.protocol.PacketInitial import PacketInitial
from src.protocol.PacketCreateSnake import PacketCreateSnake
from src.protocol.PacketPong import PacketPong
from src.protocol.PacketUpdatePosition import PacketUpdatePosition
from src.protocol.PacketCreateFood import PacketCreateFood
from src.packet.BufferTypes import *
from src.packet.ArrayBuffer import ArrayBuffer
import struct, re, time, random, math, array

class ProtocolHandler(WebSocketServerProtocol):
	current_connection = None
	current_snakeId = 0

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
		value = buffer.unpackData(int8)[0]

		if value == 115:
			# Send the initial startup packet.
			self.initial = PacketInitial(self, isBinary)
			self.initial.recieve(payload)
			self.initial.create()

			# Create the snakes enter defaults
			(x, y) = self.getRandomSpawnPoint()
			speed = gameserver.snakeTravelSpeed
			snakeId = self.allocateNewSnakeId()
			self.current_snakeId = snakeId
			angle = random.randint(0, 360) # TODO!
			# TODO! correctly pack the name field.
			values = [snakeId, x, y, angle, speed, int(self.initial.skinId[0]), len(self.initial.username), self.initial.username] # The name is a place holder, for now.

			# Create a new snake.
			self.newSnake = PacketCreateSnake(self, isBinary)
			self.newSnake.recieve(payload)
			self.newSnake.create(values)

			# Setup food, leaderboard etc...
			self.startSpawningFood(payload, isBinary)
		elif value == 112:
			self.pong = PacketPong(self, isBinary)
			self.pong.recieve(payload)
			self.pong.create()
		elif value == 101:
			for snake in gameserver.generatedSnakes:
				if snake.id == self.current_snakeId:
					self.positionUpdater = PacketUpdatePosition(self, isBinary)
					self.positionUpdater.recieve(buffer)
					self.positionUpdater.create(snake)
		else:
			print (value)

	def startSpawningFood(self, payload, isBinary):
		self.foodSpawner = PacketCreateFood(self, isBinary)
		self.foodSpawner.recieve(payload)
		self.foodSpawner.create()

	def getTimestamp(self):
		pass

	def setLastSent(self, timestamp):
		gameserver.timestamp = timestamp

	def getLastSent(self):
		return gameserver.timestamp

	def allocateNewSnakeId(self):
		return random.randint(0, gameserver.maxSnakeId)

	def getRandomSpawnPoint(self):
		x = random.randint(0, 70000)
		y = random.randint(0, 70000)
		return (x, y)

	def onClose(self, wasClean, code, reason):
		gameserver.activeConnections.remove(self.current_connection)
		self.current_connection = None

		# reset the clients snake to None
		for snake in gameserver.generatedSnakes:
			if snake.id == self.current_snakeId:
				gameserver.generatedSnakes.remove(snake)
