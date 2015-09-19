import string

from output import Output
from state import state

from extra import irc, log, log_incoming, log_outgoing
from extra.config import Config
from extra.irc.server import Clients

modechars = string.ascii_lowercase + string.ascii_uppercase

def start_client_listener():
	from twisted.internet.protocol import ServerFactory
	from twisted.protocols.basic import LineReceiver

	class IRCClientConnection(LineReceiver):
		def __init__(self, connectionIndex, state, clients):
			self.idented = False
			self.nick = None
			self.user = None
			self.host = None
			self.realname = None
			self.state = state
			self.clients = clients
			self.out = Output(self.sendLine)

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
			line = irc.Line.parse(raw_line)

			self.clientHandler.handleLine(line)

			self.idented = self.nick is not None and self.user is not None and self.realname is not None

			if self.idented and not self.state.isNick(self.nick):
				log.info('@ Ident has been completed on connection {0}'.format(self.connectionIndex))
				log.info('@ nick={0} user={1} host={2} peer={3} connection={4}'.format(
					self.nick, self.user, self.host, self.transport.getPeer(), self.connectionIndex
				)
				self.state.nicks.add(
					nick=self.nick,
					user=self.user,
					host=self.host,
					realname=self.realname,
					server=Config.hostname,
					modes='i'
				)
				self.sendCode('001', ':Welcome to ExtraIRC')
				self.sendCode('004', ' '.join([
					Config.hostname,
					Config.version,
					modechars, # usermodes [a-zA-Z]
					modechars, # channel modes
					'beIovhkl' # channel modes requiring parameters
				])
				self.sendCode('005', ' '.join([
					'DEAF=D KICKLEN=180 PREFIX=(ohv)@%+ STATUSMSG=@%+ EXCEPTS=e',
					'INVEX=I NICKLEN=18 NETWORK=extra MAXLIST=beI:100 MAXTARGETS=1'
				])
				self.sendCode('005', ' '.join([
					'CHANTYPES=# CHANLIMIT=#:500 CHANNELLEN=18 TOPICLEN=400',
					'CHANMODES=beI,k,l,{0}'.format(''.join(l for l in modechars if l not in 'beIkl')),
					'SAFELIST KNOCK AWAYLEN=200'
				])

		def __str__(self):
			return "{0}!{1}@{2}".format(self.nick, self.user, self.host)

		
	class IRCServerFactory(ServerFactory):
		protocol = IRCClientConnection

		def __init__(self):
			self.connectionIndex = 0
			self.state = state()
			self.clients = Clients(self.state)

		def buildProtocol(self):
			proto = IRCClientConnection(self.connectionIndex, self.state, self.clients)
			self.connectionIndex += 1
			return proto

	from twisted.internet import reactor
	reactor.listenTCP(6667, IRCServerFactory())
	reactor.run()
