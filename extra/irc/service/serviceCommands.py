# commands return a list of lines which will be NOTICEd back to the user
class ServiceCommands:
	def ASSOCIATE(self, line):
		pass

	def DEIDENT(self, line):
		pass

	def HELP(self, line):
		return [
			'ExtraServ ~new~ IRC Services',
			'Help is not yet implemented'
		]

	def IDENTIFY(self, line):
		pass

	def OP(self, line):
		pass

	def RECOVER(self, line):
		pass

	def REGCHAN(self, line):
		pass

	def REGISTER(self, line):
		pass

	def REGPHONE(self, line):
		pass

	def SET(self, line):
		pass

	def SETPASS(self, line):
		pass

	def STICKYLISTS(self, line):
		pass

	def STICKYMODES(self, line):
		pass

	def VALIDATE(self, line):
		pass

	def VERIFYPHONE(self, line):
		pass
