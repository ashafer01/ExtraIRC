simpleNickCmds = [
	'PRIVMSG',
	'NOTICE'
]

class Output:
	def __init__(self, function):
		self.function = function

	def as(SELF, NICK):
		def outputAs(cmd):
			SELF.function(":{0} {1}".format(NICK, cmd))
		class nickFuncs:
			def simpleCmd(self, cmd, arg, text):
				outputAs("{1} {2} :{3}".format(cmd, arg, text)
			def __getattr__(self, name):
				name = name.upper()
				if name in simpleNickCmds:
					def cmdfunc(arg, text):
						self.simpleCmd(name, arg, text)
					return cmdfunc
				else:
					raise AttributeError(name)
		return nickFuncs
