from extra.irc import client
from extra.config import Config
from extra.utils import time

class Output:
	def __init__(self, out_function):
		self.send = out_function

	def asNick(self, nick):
		def sendAsNick(text):
			self.send(":{0} {1}".format(nick, text))
		return client.Output(sendAsNick)

	def asServer(self, text):
		self.send(":{0} {1}".format(Config.hostname, text))

	def SJOIN(self, nick, channel):
		self.asServer("SJOIN {0} {1} + :{2}".format(time(), channel, nick))

	def SVSJOIN(self, nick, channel):
		self.asServer("SVSJOIN {0} {1} {2}".format(nick, channel, time()))

	def SVSNICK(self, oldnick, newnick):
		self.asServer("SVSNICK {0} {1} {2}".format(oldnick, newnick, time()))

	def NICK(self, **params):
		# NICK NickServ 2 1433794654 +io NickServ dot.cs.wmich.edu dot.cs.wmich.edu 0 :Nickname Services
		params['ts'] = time()
		params['myHostname'] = Config.hostname
		self.send("NICK {nick} 1 {ts} {mode} {user} {host} {myHostname} 0 :{name}".format(**params))

	def ERROR(self, text):
		self.send("ERROR :{0}".format(text))

