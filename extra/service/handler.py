import ..log

class handler:
	def __init__(self, endpoint):
		log.debug1('Constructed new extra.service.handler')
		self.endpoint = endpoint

	def ERROR(self, line):
		log.fatal("Received ERROR line: {0}".format(line.text))
		sys.exit(1)

	def PING(self, line):
		self.endpoint.send("PONG :{0}".format(line.text)

	def AWAY(self, line):
		pass

	def EOB(self, line):
		log.debug("Got EOB line")


