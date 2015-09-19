from twisted.internet.protocol import ServerFactory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor

import extra

class ExtraClientConnection(LineReceiver):
	def __init__(self, connectionIndex, state, clients, roleModule):
		self.idented = False
		self.nick = None
		self.user = None
		self.host = None
		self.realname = None

		self.state = state
		self.clients = clients

		self.connectionIndex = connectionIndex
		self.clients.conn_objects.append(self)
		self.clientHandler = roleMoudle.clients.Handler(self)

	def sendLine(self, line):
		extra.log_outgoing(line)
		LineReceiver.sendLine(self, line)

	def lineReceived(self, raw_line):
		extra.log_incoming(raw_line)
		self.clientHandler.handleLine(raw_line)

	def __str__(self):
		return "{0}!{1}@{2}".format(self.nick, self.user, self.host)

	
class ExtraServerFactory(ServerFactory):
	protocol = ExtraClientConnection

	def __init__(self, roleModule):
		self.connectionIndex = 0
		self.state = roleModule.State()
		self.clients = roleModule.clients.Collection(self.state)

	def buildProtocol(self):
		proto = ExtraClientConnection(self.connectionIndex, self.state, self.clients)
		self.connectionIndex += 1
		return proto

def start(roleModule):
	reactor.listenTCP(6667, ExtraServerFactory(roleModule))
	reactor.run()
