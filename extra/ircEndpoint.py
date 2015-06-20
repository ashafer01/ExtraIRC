import log
import irc

class ircEndpoint:
	def __init__(self, handler):
		self.write = None
		self.handler = handler(self, log)

	def handleLine(self, raw_line):
		raw_line = raw_line.strip()
		log.info(log.color.cyan("<= {0}".format(raw_line)))

		line = irc.Line.parse(raw_line)
		try:
			getattr(self.handler, line.cmd)(line)
		except NameError:
			# unhandled IRC command
			pass

	def send(self, line):
		log.info(log.color.green("=> {0}".format(line)))
		self.write(line)

def start_twisted(HANDLER):
	from twisted.internet.protocol import ClientFactory
	from twisted.internet.endpoints import TCP4ClientEndpoint
	from twisted.protocols.basic import LineReceiver

	class Uplink(LineReceiver):
		def __init__(self, **kwargs)
			self.ircEndpoint = ircEndpoint(kwargs['handler'])
			self.ircEndpoint.write = self.sendLine

		def lineReceived(self, line):
			self.ircEndpoint.handleLine(line)

	class UplinkFactory(ClientFactory):
		protocol = Uplink

		def __init__(self, **kwargs):
			self.init_kwargs = kwargs

		def buildProtocol(self, addr):
			return Uplink(**self.init_kwargs)

	from twisted.internet import reactor
	reactor.connectTCP('localhost', 9999, UplinkFactory(handler=HANDLER))
	reactor.run()

def start_stdio(HANDLER):
	import extra
	import sys
	ircEndpoint = extra.ircEndpoint(HANDLER)
	def write(line):
		print line
	ircEndpoint.write = write
	while True:
		ircEndpoint.handleLine(sys.stdin.readline())

