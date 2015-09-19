from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor

import extra

class Uplink(LineReceiver):
	def __init__(self, state, roleModule):
		self.state = state
		self.handler = roleModule.Handler(self)

	def sendLine(self, line):
		extra.log_outgoing(line)
		LineReceiver.sendLine(self, line)

	def lineReceived(self, raw_line):
		extra.log_incoming(raw_line)
		self.handler.handleLine(raw_line)

	def connectionMade(self):
		self.handler.ident()

class UplinkFactory(ClientFactory):
	protocol = Uplink

	def __init__(self, roleModule):
		self.state = roleModule.State()
		self.roleModule = roleModule

	def buildProtocol(self, addr):
		return Uplink(self.state)

def start(roleModule):
	extra.log.info('Starting twisted uplink to {0}:{1}'.format(extra.config.uplink.host, extra.config.uplink.port))
	reactor.connectTCP(extra.config.uplink.host, extra.config.uplink.port, UplinkFactory(roleModule))
	reactor.run()
