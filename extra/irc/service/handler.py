import sys
from .. import log

class handler:
	def __init__(self, endpoint):
		log.debug1('Constructed new extra.service.handler')
		self.endpoint = endpoint

	def ERROR(self, line):
		log.fatal("Received ERROR line: {0}".format(line.text))
		sys.exit(1)

	def PING(self, line):
		self.endpoint.send("PONG :{0}".format(line.text))

	def AWAY(self, line):
		log.debug('Got AWAY')

	def EOB(self, line):
		log.debug("Got EOB")

	def SERVER(self, line):
		log.debug("Got SERVER")

	def NICK(self, line):
		log.debug('Got NICK line')
		if line.prefix is None or self.endpoint.state.isServer(line.prefix):
			log.info('Got new nick {0}'.format(line.args[0]))
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
		log.debug('Got SJOIN')

	def JOIN(self, line):
		log.debug('Got JOIN')

	def PART(self, line):
		log.debug('Got PART')

	def MODE(self, line):
		log.debug('Got MODE')

	def KICK(self, line):
		log.debug('Got KICK')

	def QUIT(self, line):
		log.debug('Got QUIT')

	def SQUIT(self, line):
		log.debug('Got SQUIT')

	def PRIVMSG(self, line):
		log.debug('Got PRIVMSG')
