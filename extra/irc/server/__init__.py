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

			self.connectionIndex = connectionIndex
			clients.conn_objects.append(self)

		def lineReceived(self, raw_line):
			log_incoming(raw_line)
			line = irc.Line.parse(raw_line)

			if line.cmd == 'NICK':
				self.nick = line.args[0]
			elif line.cmd == 'USER':
				self.user = line.args[0]
				self.host = line.args[1]
				self.realname = line.text
			elif line.cmd == 'JOIN':
				channel = line.args[0]
				clients.relayChannel(line.handle, channel, line.raw)
				state.channels.addMember(channel, self.nick)

			self.idented = self.nick is not None and self.user is not None and self.realname is not None

			if self.idented and not state.isNick(self.nick):
				state.nicks.add(nick=self.nick,
					user=self.user,
					host=self.host,
					realname=self.realname,
					server=Config.hostname,
					modes='i'
				)

		def __str__(self):
			return "{0}!{1}@{2}".format(self.nick, self.username, Config.hostname)

		
	class IRCServerFactory(ServerFactory):
		protocol = IrcClientConnection

		def __init__(self):
			self.connectionIndex = 0

		def buildProtocol(self):
			proto = IRCClientConnection(self.connectionIndex)
			self.connectionIndex += 1
			return proto

