import sys
import collections

from extra import log
from extra.utils import time
from extra.config import Config
from output import Output

class UplinkNotAuthedError(Exception):
	pass

class handler:
	def __init__(self, endpoint):
		log.debug('Constructed new extra.irc.server.handler')
		self.endpoint = endpoint
		self.out = Output(self.endpoint.send)
		self.uplinkAuthed = False

	def ident(self):
		log.debug("Starting service ident")
		self.out.send("PASS {0} :TS".format(Config.password('uplink_send')))
		self.out.send("CAPAB :ENCAP EX IE HOPS SVS CHW QS EOB KLN GLN KNOCK UNKLN DLN UNDLN")
		self.out.send("SID {0} 1 {1} :{2}".format(Config.hostname, Config.token, Config.info))
		self.out.send("SERVER {0} 1 :{1}".format(Config.hostname, Config.info))
		self.out.send("SVINFO 6 5 0 :{0}".format(time()))
		log.debug("Completed service ident")

	def __getattr__(self, name):
		def unhandled(line):
			log.debug2("{0} UNHANDLED > {1}".format(name, line))
		return unhandled

	def handleLine(self, line):
		try:
			getattr(self, line.cmd)(line)
		except UplinkNotAuthedError:
			log.error('Uplink server is not authenticated for {0} from {1}'.format(line.cmd, line.prefix))

	def checkUplinkAuthed(self):
		if self.uplinkAuthed:
			log.debug3('Server is authenticated')
		else:
			raise UplinkNotAuthedError()

	def ERROR(self, line):
		log.fatal("Received ERROR line: {0}".format(line.text))
		sys.exit(1)

	def PING(self, line):
		self.out.send("PONG :{0}".format(line.text))

	def AWAY(self, line):
		log.debug2('Got AWAY')

	def EOB(self, line):
		log.debug2("Got EOB")
		self.checkUplinkAuthed()

		log.debug('Setting up handles')
		for nick in Config.handles:
			self.out.NICK(**Config.handles[nick])
			for channel in Config.channels:
				log.debug('Joining {0} to {1}'.format(nick, channel))
				self.out.SJOIN(nick, channel)

	def PASS(self, line):
		log.debug2("Got PASS")
		if line.prefix is None:
			log.info("Checking PASS from uplink server")
			if line.args[0] != Config.password('uplink_accept'):
				raise Exception('Uplink server supplied invalid password')
			else:
				log.info('Uplink server PASS OK')
				self.uplinkAuthed = True
		else:
			log.debug1('Got PASS from {0}'.format(line.prefix))

	def SERVER(self, line):
		log.debug2("Got SERVER")
		self.checkUplinkAuthed()
		self.endpoint.state.servers.add(name=line.args[0], token=line.args[1], desc=line.text)
		if line.prefix is None:
			self.endpoint.uplinkServer = line.args[0]
		log.debug2('Finished SERVER handling')

	def NICK(self, line):
		log.debug2('Got NICK line')
		self.checkUplinkAuthed()
		if line.prefix is None or self.endpoint.state.isServer(line.prefix):
			self.endpoint.state.nicks.add(
				nick=line.args[0],
				user=line.args[4],
				host=line.args[5],
				server=line.args[6],
				modes=line.args[3][1:],
				realname=line.text
			)
		elif self.endpoint.state.isNick(line.args[0]):
			self.endpoint.state.changeNick(line.handle.nick, line.args[0])
		else:
			log.warning('Input to NICK is an unhandled condition')
		log.debug2('Finished NICK handling')

	def SJOIN(self, line):
		log.debug2('Got SJOIN')
		self.checkUplinkAuthed()

		chan = line.args[1]
		cmodes = line.args[2][1:]
		newchan = {'channel':chan, 'modes':cmodes, 'mode_k':'', 'mode_l':''}

		# handle mode args
		mode_args = collections.deque(line.args[3:] + ['',''])
		for modechar in cmodes:
			if modechar in 'kl':
				newchan['mode_' + modechar] = mode_args.popleft()
			elif modechar in 'ohvbeI':
				raise Exception('List mode in SJOIN')

		self.endpoint.state.channels.add(**newchan)

		# process names list
		names = line.text.split()
		for name in names:
			chanmodes = ''
			while name[0] in Config.modeSymbolMap:
				chanmodes += Config.modeSymbolMap[name[0]]
				name = name[1:]

			if self.endpoint.state.isNick(name):
				self.endpoint.state.channels.addMember(chan, name)
				for c in chanmodes:
					self.endpoint.state.channels.addToModelist(chan, c, name)
			else:
				log.warning('Got unknown nick in SJOIN')
		log.debug2('Finished SJOIN handling')

	def JOIN(self, line):
		log.warning('Got standard JOIN message > {0}'.format(line))
		self.checkUplinkAuthed()

	def PART(self, line):
		log.debug2('Got PART')
		self.checkUplinkAuthed()
		self.endpoint.state.channels.removeMember(line.args[0], line.handle.nick)
		log.debug2('Finished PART handling')

	def MODE(self, line):
		log.debug2('Got MODE')
		self.checkUplinkAuthed()
		target = line.args[0].lower()
		modeargs = collections.deque(line.args[2:])
		if self.endpoint.state.isChannel(target):
			log.debug('Got chanmode change')
			chan = target
			chanobj = self.endpoint.state.channels.get(chan)
			modes = line.args[1]
			op = None
			changeParams = {'channel':chan,'modes':set(chanobj.modes)}
			for c in modes:
				if c in '+-':
					op = c
					continue
				if op is None:
					raise Exception('Malformed MODE')
				log.debug1('Found chanmode {0} {1}'.format(chan, op + c))
				if c in 'ohvbeI': # list modes
					log.debug2('Taking argument for {0}'.format(op + c))
					value = modeargs.popleft()
					if op == '+':
						self.endpoint.state.channels.addToModelist(chan, c, value)
					else:
						self.endpoint.state.channels.removeFromModelist(chan, c, value)
				elif c in 'kl': # single-argument modes
					if op == '+':
						log.debug2('Taking argument for {0}'.format(op + c))
						value = modeargs.popleft()
						changeParams['mode_' + c] = value
						changeParams['modes'].add(c)
					else:
						changeParams['mode_' + c] = ''
						changeParams['modes'].discard(c)
				else: # mode flag
					if op == '+':
						changeParams['modes'].add(c)
					else:
						changeParams['modes'].discard(c)
			self.endpoint.state.channels.setModes(**changeParams)
		elif self.endpoint.state.isNick(target):
			log.debug('Got usermode change')
			nick = target
			modes = line.text
			nickobj = self.endpoint.state.nicks.get(nick)
			newmodes = set(nickobj.modes)
			op = None
			for c in modes:
				if c in '+-':
					op = c
					continue
				if op is None:
					raise Exception('Malformed MODE')
				log.debug1('Found usermode {0} {1}{2}'.format(nick, op, c))
				if op == '+':
					newmodes.add(c)
				else:
					newmodes.discard(c)
			self.endpoint.state.nicks.setModes(nick, newmodes)
		else:
			log.error('Unknown MODE target')
		log.debug2('Finished MODE handling')

	def KICK(self, line):
		log.debug('Got KICK')
		self.checkUplinkAuthed()
		self.endpoint.state.channels.removeMember(line.args[0], line.args[1])
		log.debug2('Finished KICK handling')

	def QUIT(self, line):
		log.debug('Got QUIT')
		self.checkUplinkAuthed()
		self.endpoint.state.removeNick(line.handle.nick)
		log.debug2('Finished QUIT handling')

	def SQUIT(self, line):
		log.debug('Got SQUIT')
		if line.prefix == Config.hostname:
			log.error('Server {0} is killing me: {1}'.format(line.args[0], line.text))
		else:
			log.notice('Server {0} has quit {1}'.format(line.prefix, line.text))
			self.endpoint.state.servers.remove(line.prefix)
		log.debug2('Finished SQUIT handling')

	def PRIVMSG(self, line):
		log.debug('Got PRIVMSG')
		self.checkUplinkAuthed()
