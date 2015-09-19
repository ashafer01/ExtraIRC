import log
import irc
from extra import log_incoming, log_outgoing

def start_twisted(endpointModule):
	log.debug('Using twisted uplink')
	from twisted.internet.protocol import ClientFactory
	from twisted.protocols.basic import LineReceiver

	class Uplink(LineReceiver):
		def __init__(self, state):
			self.handler = endpointModule.handler(self)
			self.state = state

		def sendLine(self, line):
			log_outgoing(line)
			LineReceiver.sendLine(self, line)

		def lineReceived(self, raw_line):
			log_incoming(raw_line)
			line = irc.Line.parse(raw_line)
			if line.prefix is not None:
				nick_obj = self.state.nicks.get(line.prefix)
				if nick_obj is not None:
					line.handle.nick = nick_obj.nick
					line.handle.user = nick_obj.user
					line.handle.host = nick_obj.host

			self.handler.handleLine(line)

		def connectionMade(self):
			self.handler.ident()

	class UplinkFactory(ClientFactory):
		protocol = Uplink

		def __init__(self, **kwargs):
			self.state = endpointModule.state()

		def buildProtocol(self, addr):
			return Uplink(self.state)

	from twisted.internet import reactor
	log.notice('Connecting to uplink')
	reactor.connectTCP('localhost', 9998, UplinkFactory())
	reactor.run()

def start_stdio(endpointModule):
	import sys
	def stderr_writeline(text):
		sys.stderr.write(text + "\n")
	log.write_line = stderr_writeline
	log.debug('Using stdio uplink')

	class Uplink:
		def __init__(self):
			self.handler = endpointModule.handler(self)
			self.state = endpointModule.state()
		def sendLine(self, line):
			log_outgoing(line)
			print line

	endpoint = Uplink()
	endpoint.handler.ident()

	log.notice('Starting stdin loop')
	while True:
		raw_line = sys.stdin.readline().strip()
		log_incoming(raw_line)
		endpoint.handleLine(raw_line)

def setup_argparse_opts(parser):
	group = parser.add_mutually_exclusive_group()
	group.add_argument('--twisted',
		dest='run',
		action='store_const',
		const=start_twisted,
		help='Use twisted to connect to the uplink server (default)'
	)
	group.add_argument('--stdio',
		dest='run',
		action='store_const',
		const=start_stdio,
		help='Accept IRC commands on stdin and reply on stdout'
	)
