from state import state

class _Clients:
	def __init__(self):
		self.conn_objects = []
		self.state = state()

	# relay message to all connected clients
	def relayAll(self, fromHandle, text):
		for conn in self.conn_objects:
			if conn.idented:
				conn.sendLine(":{0} {1}".format(fromHandle, text))

	# relay message to all clients in the given channel
	def relayChannel(self, fromHandle, channel, text):
		for conn in self.conn_objects:
			if conn.idented and conn.nick in self.state.channels.getMembers(channel):
				conn.sendLine(":{0} {1}".format(fromHandle, text))

clients = _Clients()

