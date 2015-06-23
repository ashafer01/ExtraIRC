import inspect
from extra import utils

class servCommand(object):
	summary = '?'

	@classmethod
	def help(cls, _):
		return ['No help for '+cls.__name__]

# commands return a list of lines which will be NOTICEd back to the user
class ServiceCommands:
	@classmethod
	def getSummaryDict(cls):
		ret = {}
		for prop in dir(cls):
			propobj = getattr(cls, prop)
			if inspect.isclass(propobj) and issubclass(propobj, servCommand):
				ret[prop] = getattr(cls, prop).summary
		return ret

	class ASSOCIATE(servCommand):
		summary = 'Associate your current nickname with your registered username'
		usage = 'ASSOCIATE <password>'

		@classmethod
		def help(cls, arg_str):
			return [
				'Usage: ' + cls.usage,
				cls.summary
			]

		def __call__(self, line):
			pass

	class DEIDENT(servCommand):
		summary = 'Remove identification for this connection'
		def __call__(self, line):
			pass

	class HELP(servCommand):
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
				if hasattr(ServiceCommands, subcmd):
					return getattr(ServiceCommands, subcmd).help(arg_str)
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

	class IDENTIFY(servCommand):
		summary = 'Identify yourself with your password'
		def __call__(self, line):
			pass

	class OP(servCommand):
		summary = 'Get channel operator privileges on a channel you own'
		def __call__(self, line):
			pass

	class RECOVER(servCommand):
		summary = 'Recover one of your associated nicknames in use by someone else'
		def __call__(self, line):
			pass

	class REGCHAN(servCommand):
		summary = 'Register a channel'
		def __call__(self, line):
			pass

	class REGISTER(servCommand):
		summary = 'Register your username'
		def __call__(self, line):
			pass

	class REGPHONE(servCommand):
		summary = 'Associate a verified phone number with a nickname'
		def __call__(self, line):
			pass

	class SET(servCommand):
		summary = 'Change various settings'
		def __call__(self, line):
			pass

	class SETPASS(servCommand):
		summary = 'Change your password (must be identified)'
		def __call__(self, line):
			pass

	class STICKYLISTS(servCommand):
		summary = 'Make mode lists on a registered channel "sticky"'
		def __call__(self, line):
			pass

	class STICKYMODES(servCommand):
		summary = 'Make simple modes on a registered channel "sticky"'
		def __call__(self, line):
			pass

	class VALIDATE(servCommand):
		summary = 'Determine if the user of a nickname is valid'
		def __call__(self, line):
			pass

	class VERIFYPHONE(servCommand):
		summary = 'Verify your phone number and associate with your username'
		def __call__(self, line):
			pass
