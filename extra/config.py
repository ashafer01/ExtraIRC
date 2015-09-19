import utils

def loadConfig():
	pass

class Config:
	def __init__(self)
		self.hostname = 'extrastout.defiant.worf.co'
		self.token = '0ES'
		self.info = 'ExtraServ ~new~ IRC Services for Hybrid'
		self.version = '0.9'

		self.serviceHandle = 'ExtraServ'

		self.handles = utils.DictObject({
			'ExtraServ': {
				'nick':'ExtraServ',
				'mode':'+io',
				'user':'ExtraServ',
				'host':'extra.worf.co',
				'name':'ExtraServ ~new~ IRC Services for Hybrid'
			}
		})

		self.channels = [
			'#alex'
		]

		self.modeSymbolMap = {
			'@':'o',
			'%':'h',
			'+':'v'
		}

		self.uplink = utils.DictObject({
			'host': 'localhost',
			'port': 9999
		})

	def password(self, pw_name):
		with open('{1}/passwords/{0}.pw'.format(pw_name, self.base_dir), 'r') as f:
			return f.readline().strip()
