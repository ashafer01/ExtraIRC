from twisted.internet.protocol import ClientFactory
from twisted.internet.endpoints import TCP4ClientEndpoint
from twisted.protocols.basic import LineReceiver

class ServerUplink(LineReceiver):
	def __init__(self, **kwargs)
		self.ircEndpoint = kwargs['ircEndpointClass'](**kwargs)
		self.ircEndpoint.write = self.sendLine

	def lineReceived(self, line):
		self.ircEndpoint.handleLine(line)

class ServerUplinkFactory(ClientFactory):
	protocol = ServerUplink

	def __init__(self, **kwargs):
		self.init_kwargs = kwargs

	def buildProtocol(self, addr):
		return ServerUplink(**self.init_kwargs)

