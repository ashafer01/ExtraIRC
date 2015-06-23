import inspect
from extra import utils

class userCommand(object):
	pass

# commands return a list of lines which will be NOTICEd back to the user
class ServiceCommands:
	@classmethod
	def getSummaryDict(cls):
		ret = {}
		for prop in dir(cls):
			propobj = getattr(cls, prop)
			if inspect.isclass(propobj) and issubclass(propobj, userCommand):
				ret[prop] = getattr(cls, prop).summary
		return ret

	class ASSOCIATE(userCommand):
		def __call__(self, line):
			pass

		summary = 'Associate your current nickname with your registered username'
		usage = 'ASSOCIATE <password>'

		@classmethod
		def help(cls, arg_str):
			return [
				'Usage: ' + cls.usage,
				cls.summary
			]

	class DEIDENT(userCommand):
		summary = 'Remove identification for this connection'
		def __call__(self, line):
			pass

	class HELP(userCommand):
		summary = 'Obtain information about how to use service commands'
		usage = 'HELP <command> [...]'

		@classmethod
		def help(cls, arg_str):
			return [
				'Usage: ' + cls.usage,
				cls.summary
			]

		def __call__(self, line):
			try:
				arg_str = line.text.split(' ', 1)[1].upper()
			except IndexError:
				arg_str = ''

			ret = []

			if len(arg_str) > 0:
				subcmd, arg_str = arg_str.split(' ', 1) + ['']
				if hasattr(self, subcmd):
					cmdclass = getattr(self, subcmd)
					if hasattr(cmdclass, 'help'):
						return cmdclass.help(arg_str)
					else:
						return ['No help for ' + subcmd]
				else:
					ret += ['Unknown command ' + subcmd, ' ']
			summaryDict = ServiceCommands.getSummaryDict()

			# find col widths
			maxlen = 0
			for cmd in summaryDict:
				n = len(cmd)
				if n > maxlen:
					maxlen = n
			l_colwidth = maxlen+1
			r_colwidth = 78-l_colwidth

			# build output
			fmt = '{0:>' + str(l_colwidth) + '}  {1:<' + str(r_colwidth) + '}'
			for cmd in summaryDict:
				summary = summaryDict[cmd]
				if len(summary) > r_colwidth:
					summary_lines = utils.smart_split(summary, r_colwidth)
					ret.append(fmt.format(cmd, summary_lines[0]))
					for l in summary_lines[1:]:
						ret.append(fmt.format('', l))
				else:
					ret.append(fmt.format(cmd, summary))
			return ret

	class IDENTIFY(userCommand):
		summary = 'Identify yourself with your password'
		def __call__(self, line):
			pass

	class OP(userCommand):
		summary = 'Get channel operator privileges on a channel you own'
		def __call__(self, line):
			pass

	class RECOVER(userCommand):
		summary = 'Recover one of your associated nicknames in use by someone else'
		def __call__(self, line):
			pass

	class REGCHAN(userCommand):
		summary = 'Register a channel'
		def __call__(self, line):
			pass

	class REGISTER(userCommand):
		summary = 'Register your username'
		def __call__(self, line):
			pass

	class REGPHONE(userCommand):
		summary = 'Associate a verified phone number with a nickname'
		def __call__(self, line):
			pass

	class SET(userCommand):
		summary = 'Change various settings'
		def __call__(self, line):
			pass

	class SETPASS(userCommand):
		summary = 'Change your password (must be identified)'
		def __call__(self, line):
			pass

	class STICKYLISTS(userCommand):
		summary = 'Make mode lists on a registered channel "sticky"'
		def __call__(self, line):
			pass

	class STICKYMODES(userCommand):
		summary = 'Make simple modes on a registered channel "sticky"'
		def __call__(self, line):
			pass

	class VALIDATE(userCommand):
		summary = 'Determine if the user of a nickname is valid'
		def __call__(self, line):
			pass

	class VERIFYPHONE(userCommand):
		summary = 'Verify your phone number and associate with your username'
		def __call__(self, line):
			pass
