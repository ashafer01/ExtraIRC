import log
import irc

class ircEndpoint:
	def __init__(self, writefunc, handlerClass, state):
		self.write = writefunc
		self.handler = handlerClass(self)
		self.state = state

	def handleLine(self, raw_line):
		raw_line = raw_line.strip()
		log.info(log.color.cyan("<= {0}".format(raw_line)))

		line = irc.Line.parse(raw_line)
		if line.prefix is not None:
			nick_obj = self.state.nicks.get(line.prefix)
			if nick_obj is not None:
				line.handle.nick = nick_obj.nick
				line.handle.user = nick_obj.user
				line.handle.host = nick_obj.host
		try:
			getattr(self.handler, line.cmd)(line)
		except AttributeError as e:
			self.handler._unhandled(line)
			log.debug3(str(e))

	def send(self, line):
		log.info(log.color.green("=> {0}".format(line)))
		self.write(line)

