simpleCmds = [
	'PRIVMSG',
	'NOTICE',
	'JOIN',
	'PART',
]

textonlyCmds = [
	'QUIT'
]

class Output:
	def __init__(self, out_function):
		self.out_function = out_function

	def simpleCmd(self, cmd, arg, text):
		self.out_function("{0} {1} :{2}".format(cmd, arg, text))

	def textonlyCmd(self, cmd, text):
		self.out_function("{0} :{1}".format(cmd, text))

	def __getattr__(self, name):
		if name in simpleCmds:
			def cmdfunc(arg, text):
				self.simpleCmd(name, arg, text)
			return cmdfunc
		elif name in textonlyCmds:
			def cmdfunc(text):
				self.textonlyCmd(name, text)
			return cmdfunc
		else:
			raise AttributeError(name)
