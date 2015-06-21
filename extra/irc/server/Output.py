from extra.irc import client.Output
from extra.config import Config
from extra.utils import time

class Output:
	def __init__(self, out_function):
		self.send = out_function

	def as(self, nick):
		def asNick(text):
			self.send(":{0} {1}".format(nick, text))
		return client.Output(asNick)

	def asServer(self, text):
		self.send(":{0} {1}".format(Config.hostname, text))

	def SJOIN(self, nick, channel):
		self.asServer("SJOIN {0} {1} + :{2}".format(time(), channel, nick))

	def SVSJOIN(self, nick, channel):
		self.asServer("SVSJOIN {0} {1} {2}".format(nick, channel, time()))

	def SVSNICK(self, oldnick, newnick):
		self.asServer("SVSNICK {0} {1} {2}".format(oldnick, newnick, time()))

