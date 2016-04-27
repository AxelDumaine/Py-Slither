from autobahn.asyncio.websocket import WebSocketServerFactory
from src.protocol.ProtocolHandler import ProtocolHandler
from src.notify.Notifyer import Notifyer

try:
	import asyncio
except:
	raise ImportError('You need asyncio to run the gameserver!')

import sys

class WebSocket(WebSocketServerFactory):
	notify = Notifyer.setupClassNotify('WebSocket')

	def __init__(self, socketAddress, socketPort):
		WebSocketServerFactory.__init__(self, u"ws://%s:%d" % (socketAddress, socketPort), False)
		self.protocol = ProtocolHandler
		# Lets keep track of the address and port for use later.
		self.socketAddress = socketAddress
		self.socketPort = socketPort
		# Some stuff for the protocol...
		self.activeConnections = []
		self.generatedSnakes = []
		self.maxSnakeId = 100
		self.timestamp = 0
		self.snakeTravelSpeed = 10
		self.generatedFood = []

	def startServer(self):
		self.notify.setNotifyInfo('Preparing the gameserver to accept connections...')
		self.loop = asyncio.get_event_loop()
		self.coro = self.loop.create_server(self, '%s' % (self.socketAddress), self.socketPort)
		self.server = self.loop.run_until_complete(self.coro)

		try:
			self.notify.setNotifyInfo('The gameserver is running on: %s:%d.' % (self.socketAddress, self.socketPort))
			self.loop.run_forever()
		except KeyboardInterrupt:
			self.stopServer()

	def stopServer(self):
		try:
			self.notify.setNotifyInfo('Shutting down the gameserver, please wait...')
			self.close()
		except:
			pass # TODO: How did this happen?
		finally:
			self.loop.close()

	def getAllPlayers(self):
		return len(self.activeConnections)