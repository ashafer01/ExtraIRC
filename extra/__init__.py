import log
import TerminalColor
from state import state
from ircEndpoint import ircEndpoint

def start_twisted(HANDLER):
	log.debug('Using twisted')
	from twisted.internet.protocol import ClientFactory
	from twisted.internet.endpoints import TCP4ClientEndpoint
	from twisted.protocols.basic import LineReceiver

	class Uplink(LineReceiver):
		def __init__(self):
			self.ircEndpoint = ircEndpoint(self.sendLine, HANDLER, state())

		def lineReceived(self, line):
			self.ircEndpoint.handleLine(line)

		def connectionMade(self):
			self.ircEndpoint.handler.ident()

	class UplinkFactory(ClientFactory):
		protocol = Uplink

		def __init__(self, **kwargs):
			self.init_kwargs = kwargs

		def buildProtocol(self, addr):
			return Uplink(**self.init_kwargs)

	from twisted.internet import reactor
	log.notice('Connecting to uplink')
	reactor.connectTCP('localhost', 9998, UplinkFactory())
	reactor.run()

def start_stdio(HANDLER):
	log.debug('Using stdio')
	import sys
	def write(line):
		print line
	_ircEndpoint = ircEndpoint(write, HANDLER, state())
	_ircEndpoint.write = write
	log.notice('Starting stdin loop')
	while True:
		_ircEndpoint.handleLine(sys.stdin.readline())
