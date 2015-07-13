import string

from output import Output
from handler import handler
from handler import UplinkNotAuthedError
from state import state

from extra import irc, log_incoming, log_outgoing
from extra.config import Config

class _Clients:
	def __init__(self):
		self.conn_objects = []

	def relayAll(self, fromHandle, text):
		for conn in self.conn_objects:
			if conn.idented:
				conn.sendLine(":{0} {1}".format(fromHandle, text))

	def relayChannel(self, fromHandle, channel, text):
		for conn in self.conn_objects:
			if conn.idented and state.channels.getMembers(channel):

clients = _Clients()
modechars = string.ascii_lowercase + string.ascii_uppercase

def start_client_listener():
	from twisted.internet.protocol import ServerFactory
	from twisted.protocols.basic import LineReceiver

	class IRCClientConnection(LineReceiver):
		def __init__(self, connectionIndex):
			self.idented = False
			self.nick = None
			self.user = None
			self.host = None
			self.realname = None
			self.state = state()
			self.out = Output(self.sendLine)

			self.connectionIndex = connectionIndex
			clients.conn_objects.append(self)

		def sendCode(self, code, text):
			self.out.asServer('{0} {1} {2}'.format(code, self.nick, text)

		def lineReceived(self, raw_line):
			log_incoming(raw_line)
			line = irc.Line.parse(raw_line)

			if line.cmd == 'NICK':
				log.debug1('Got client NICK on connection {0}'.format(self.connectionIndex))
				self.nick = line.args[0]
				if self.idented:
					log.debug('Got client nick change on connection {0}'.format(self.connectionIndex))
					self.state.changeNick(line.handle.nick, self.nick)
				else:
					log.debug2('Not changing nick in state table')
			elif line.cmd == 'USER':
				log.debug1('Got client USER on connection {0}'.format(self.connectionIndex))
				if not self.idented:
					self.user = line.args[0]
					self.host = line.args[1]
					self.realname = line.text
			elif line.cmd == 'JOIN':
				channel = line.args[0]
				clients.relayChannel(line.handle, channel, line.raw)
				self.state.channels.addMember(channel, line.handle.nick)
			elif line.cmd == 'PART':
				channel = line.args[0]
				clients.relayChannel(line.handle, channel, line.raw)
				self.state.channels.removeMember(channel, line.handle.nick)
			elif line.cmd == 'QUIT':
				self.state.removeNick(line.handle.nick)
			elif line.cmd == 'MOTD':
				self.sendCode('375', ':=== Message of the day ===')
				self.sendCode('372', ':Message of the day is not yet configurable!')
				self.sendCode('376', ':=== End MOTD ===')

			self.idented = self.nick is not None and self.user is not None and self.realname is not None

			if self.idented and not self.state.isNick(self.nick):
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
		protocol = IrcClientConnection

		def __init__(self):
			self.connectionIndex = 0

		def buildProtocol(self):
			proto = IRCClientConnection(self.connectionIndex)
			self.connectionIndex += 1
			return proto

