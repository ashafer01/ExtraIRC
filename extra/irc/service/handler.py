from extra import log
from extra.irc import server
from extra.config import Config
from serviceCommands import ServiceCommands

class handler(server.handler):
	def __init__(self, endpoint):
		log.debug('Constructed new extra.irc.service.handler')
		self.endpoint = endpoint
		self.out = server.Output(self.endpoint.sendLine)
		self.cmds = ServiceCommands()

	def PRIVMSG(self, line):
		server.handler.PRIVMSG(self, line)
		log.debug1('Handling PRIVMSG as service')

		if line.args[0] == Config.serviceHandle:
			log.debug('Got private message to service handle ' + Config.serviceHandle)
			cmd = line.text.strip().split()[0].upper()
			try:
				cmdclass = getattr(self.cmds, cmd)
				log.debug('Running command ' + cmd)
			except AttributeError:
				log.debug1('Not a command')
				return
			notices = cmdclass()(line)
			for notice in notices:
				self.out.asNick(Config.serviceHandle).NOTICE(line.handle.nick, notice)
		else:
			log.debug1('Ignoring non-PM PRIVMSG')

	def MODE(self, line):
		server.handler.MODE(self, line)

	def NICK(self, line):
		server.handler.NICK(self, line)

	def SJOIN(self, line):
		server.handler.SJOIN(self, line)
