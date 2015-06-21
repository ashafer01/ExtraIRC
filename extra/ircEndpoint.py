import log
import irc

class ircEndpoint:
	def __init__(self, writefunc, handler, state):
		self.write = writefunc
		self.handler = handler(self)
		self.state = state

	def handleLine(self, raw_line):
		raw_line = raw_line.strip()
		log.info(log.color.cyan("<= {0}".format(raw_line)))

		line = irc.Line.parse(raw_line)
		try:
			getattr(self.handler, line.cmd)(line)
		except NameError:
			# unhandled IRC command
			pass

	def send(self, line):
		log.info(log.color.green("=> {0}".format(line)))
		self.write(line)

