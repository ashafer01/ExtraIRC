# handles client -> server commands
from extra import log
from output import Output

class handler(object):
	def __init__(self, endpoint):
		self.endpoint = endpoint
		self.out = Output(self.endpoint.sendLine)

	def handleLine(self, line):
		getattr(self, line.cmd)(line)

	def __getattr__(self, name):
		def unhandled(line):
			log.notice('{0} UNHANDLED > {0}'.format(name, line)
			self.endpoint.sendCode('421', line.cmd + ' :Unknown command')
		return unhandled
	
	# ident commands

	def NICK(self, line):
		log.debug1('Got client NICK on connection {0}'.format(self.endpoint.connectionIndex))
		self.endpoint.nick = line.args[0]
		if self.idented:
			log.debug('Got client nick change on connection {0}'.format(self.endpoint.connectionIndex))
			self.endpoint.state.changeNick(line.handle.nick, self.nick)
		else:
			log.debug2('Not changing nick in state table as ident is not complete')

	def USER(self, line):
		log.debug1('Got client USER on connection {0}'.format(self.endpoint.connectionIndex))
		if not self.idented:
			self.endpoint.user = line.args[0]
			self.endpoint.host = line.args[1]
			self.endpoint.realname = line.text
		else:
			pass

	def PASS(self, line):
		pass

	def OPER(self, line):
		pass

	# user state

	def AWAY(self, line):
		pass

	def QUIT(self, line):
		self.endpoint.state.removeNick(line.handle.nick)

	# messages

	def PRIVMSG(self, line):
		pass

	def NOTICE(self, line):
		pass

	# channel commands

	def JOIN(self, line):
		channel = line.args[0]
		self.endpoint.clients.relayChannel(line.handle, channel, line.raw)
		self.endpoint.state.channels.addMember(channel, line.handle.nick)

	def PART(self, line):
		channel = line.args[0]
		self.endpoint.clients.relayChannel(line.handle, channel, line.raw)
		self.endpoint.state.channels.removeMember(channel, line.handle.nick)

	def KICK(self, line):
		pass

	# -> MODE #channel +I
	# <- :yakko.cs.wmich.edu 346 alexnc #aluminati Nextrastout!Nextrasto@* alex!alex@yakko.cs.wmich.edu 1442454332
	def MODE(self, line):
		pass

	def INVITE(self, line):
		pass

	def KNOCK(self, line):
		pass

	def TOPIC(self, line):
		pass

	def NAMES(self, line):
		pass

	# informational/misc

	def MOTD(self, line):
		self.endpoint.sendCode('375', ':=== Message of the day ===')
		self.endpoint.sendCode('372', ':Message of the day is not yet configurable!')
		self.endpoint.sendCode('376', ':=== End MOTD ===')

	def LIST(self, line):
		pass

	def PING(self, line):
		self.out.PONG(line.text)

	def PONG(self, line):
		pass

