# handles client -> server commands
import string

from extra import log
from output import Output

modechars = string.ascii_lowercase + string.ascii_uppercase

class Handler(object):
	def __init__(self, endpoint):
		self.endpoint = endpoint
		self.out = Output(self.endpoint.sendLine)
		self.last_pong = 0

	def handleLine(self, raw_line):
		line = irc.Line.parse(raw_line)
		getattr(self, line.cmd)(line)

		self.idented = self.nick is not None and self.user is not None and self.realname is not None

		if self.endpoint.idented and not self.endpoint.state.isNick(self.nick):
			log.info('@ Ident has been completed on connection {0}'.format(self.connectionIndex))
			log.info('@ nick={0} user={1} host={2} peer={3} connection={4}'.format(
				self.nick, self.user, self.host, self.transport.getPeer(), self.connectionIndex
			)
			self.endpoint.state.nicks.add(
				nick=self.endpoint.nick,
				user=self.endpoint.user,
				host=self.endpoint.host,
				realname=self.endpoint.realname,
				server=config.hostname,
				modes='i'
			)
			self.out.sendCode('001', ':Welcome to ExtraIRC')
			self.out.sendCode('004', ' '.join([
				config.hostname,
				config.version,
				modechars, # usermodes [a-zA-Z]
				modechars, # channel modes
				'beIovhkl' # channel modes requiring parameters
			])
			self.out.sendCode('005', ' '.join([
				'DEAF=D KICKLEN=180 PREFIX=(ohv)@%+ STATUSMSG=@%+ EXCEPTS=e',
				'INVEX=I NICKLEN=18 NETWORK=extra MAXLIST=beI:100 MAXTARGETS=1'
			])
			self.out.sendCode('005', ' '.join([
				'CHANTYPES=# CHANLIMIT=#:500 CHANNELLEN=18 TOPICLEN=400',
				'CHANMODES=beI,k,l,{0}'.format(''.join(l for l in modechars if l not in 'beIkl')),
				'SAFELIST KNOCK AWAYLEN=200'
			])

	def __getattr__(self, name):
		def unhandled(line):
			log.notice('{0} UNHANDLED > {0}'.format(name, line)
			self.out.sendCode('421', line.cmd + ' :Unknown command')
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
		self.out.sendCode('375', ':=== Message of the day ===')
		self.out.sendCode('372', ':Message of the day is not yet configurable!')
		self.out.sendCode('376', ':=== End MOTD ===')

	def LIST(self, line):
		pass

	def PING(self, line):
		self.out.PONG(line.text)

	def PONG(self, line):
		pass

