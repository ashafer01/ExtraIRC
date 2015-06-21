import sys
from extra import log
from extra.irc import server.Output
from extra.utils import time

class handler:
	def __init__(self, endpoint):
		log.debug1('Constructed new extra.service.handler')
		self.endpoint = endpoint
		self.out = server.Output(self.endpoint.send)
		self._ident()

	def _ident(self):
		log.debug("Starting service ident")
		self.out.send("PASS {0} :{1}".format(Config.password('uplink_send'), time()))
		self.out.send("CAPAB :ENCAP EX IE HOPS SVS CHW QS EOB KLN GLN KNOCK UNKLN DLN UNDLN")
		self.out.send("SID {0} 1 {1} :{2}".format(Config.hostname, Config.token, Config.info))
		self.out.send("SERVER {0} 1 :{1}".format(Config.hostname, Config.info))
		self.out.send("SVINFO 6 5 0 :{0}".format(time()))
		log.debug("Completed service ident")

	def _unhandled(self, line):
		log.warning("UNHANDLED: {0}".format(line))

	def ERROR(self, line):
		log.fatal("Received ERROR line: {0}".format(line.text))
		sys.exit(1)

	def PING(self, line):
		self.out.send("PONG :{0}".format(line.text))

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
