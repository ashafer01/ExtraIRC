simpleCmdList = [
	'PRIVMSG',
	'NOTICE'
]

class Output:
	def __init__(self, out_function):
		self.out_function = out_function

	def simpleCmd(self, cmd, arg, text):
		self.out_function("{0} {1} :{2}".format(cmd, arg, text))

	def __getattr__(self, name):
		if name in simpleNickCmds:
			def cmdfunc(arg, text):
				self.simpleCmd(name, arg, text)
			return cmdfunc
		else:
			raise AttributeError(name)
