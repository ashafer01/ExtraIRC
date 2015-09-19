import sys

import extra

class Uplink:
	def __init__(self, roleModule):
		self.handler = roleModule.Handler(self)
		self.state = roleModule.State()
	def sendLine(self, line):
		extra.log_outgoing(line)
		print line

def start(roleModule):
	def stderr_writeline(text):
		sys.stderr.write(text + "\n")
	extra.log.write_line = stderr_writeline
	extra.log.debug('Using stdio uplink')

	endpoint = Uplink()
	endpoint.handler.ident()

	extra.log.notice('Starting stdin loop')
	while True:
		raw_line = sys.stdin.readline().strip()
		extra.log_incoming(raw_line)
		endpoint.handleLine(raw_line)
