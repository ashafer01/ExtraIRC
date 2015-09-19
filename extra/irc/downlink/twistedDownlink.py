from twisted.internet.protocol import ServerFactory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor

from extra import irc, log, config, log_incoming, log_outgoing

class IRCClientConnection(LineReceiver):
	def __init__(self, connectionIndex, state, clients):
		self.idented = False
		self.nick = None
		self.user = None
		self.host = None
		self.realname = None
		self.state = state
		self.clients = clients

		self.last_pong = 0

		self.connectionIndex = connectionIndex
		self.clients.conn_objects.append(self)
		self.clientHandler = clientHandler(self)

	def sendLine(self, line):
		log_outgoing(line)
		LineReceiver.sendLine(self, line)

	def sendCode(self, code, text):
		self.out.asServer('{0} {1} {2}'.format(code, self.nick, text))

	def lineReceived(self, raw_line):
		log_incoming(raw_line)
		self.clientHandler.handleLine(raw_line)

	def __str__(self):
		return "{0}!{1}@{2}".format(self.nick, self.user, self.host)

	
class IRCServerFactory(ServerFactory):
	protocol = IRCClientConnection

	def __init__(self, roleModule):
		self.connectionIndex = 0
		self.state = roleModule.State()
		self.clients = roleModule.ClientsCollection(self.state)

	def buildProtocol(self):
		proto = IRCClientConnection(self.connectionIndex, self.state, self.clients)
		self.connectionIndex += 1
		return proto

def start(roleModule):
	reactor.listenTCP(6667, IRCServerFactory(roleModule))
	reactor.run()
