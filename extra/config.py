import utils

def loadConfig():
	pass

class Config:
	hostname = 'extrastout.defiant.worf.co'
	token = '0ES'
	info = 'ExtraServ ~new~ IRC Services for Hybrid'

	serviceHandle = 'ExtraServ'

	handles = utils.DictObject({
		'ExtraServ': {
			'nick':'ExtraServ',
			'mode':'+io',
			'user':'ExtraServ',
			'host':'extra.worf.co',
			'name':'ExtraServ ~new~ IRC Services for Hybrid'
		}
	})

	channels = [
		'#alex'
	]

	modeSymbolMap = {
		'@':'o',
		'%':'h',
		'+':'v'
	}

	@classmethod
	def password(cls, pw_name):
		with open('{1}/passwords/{0}.pw'.format(pw_name, cls.base_dir), 'r') as f:
			return f.readline().strip()
