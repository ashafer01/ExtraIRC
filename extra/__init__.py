import log
from TerminalColor import TerminalColor
from state import state
from ircEndpoint import ircEndpoint

def start_twisted(HANDLER):
	from twisted.internet.endpoints import TCP4ClientEndpoint
	from twisted.protocols.basic import LineReceiver

	class Uplink(LineReceiver):
		def __init__(self, **kwargs)
			self.ircEndpoint = ircEndpoint(self.sendLine, kwargs['handler'], state())

		def lineReceived(self, line):
			self.ircEndpoint.handleLine(line)

	class UplinkFactory(ClientFactory):
		protocol = Uplink

		def __init__(self, **kwargs):
			self.init_kwargs = kwargs

		def buildProtocol(self, addr):
			return Uplink(**self.init_kwargs)

	from twisted.internet import reactor
	reactor.connectTCP('localhost', 9999, UplinkFactory(handler=HANDLER, state=state))
	reactor.run()

def start_stdio(HANDLER):
	import sys
	def write(line):
		print line
	_ircEndpoint = ircEndpoint(write, HANDLER, state())
	_ircEndpoint.write = write
	while True:
		_ircEndpoint.handleLine(sys.stdin.readline())
