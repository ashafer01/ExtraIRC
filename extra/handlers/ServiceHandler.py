import ..log

class ServiceHandler:
	def __init__(self, endpoint, log):
		self.endpoint = endpoint
		self.log = log

	def ERROR(self, line):
		log.fatal(log.color.red("Received ERROR line: {0}".format(line.text)))
		sys.exit(1)

	def PING(self, line):
		self.endpoint.send("PONG :{0}".format(line.text)

	def AWAY(self, line):
		pass

	def EOB(self, line):
		self.log.debug("Got EOB line")

