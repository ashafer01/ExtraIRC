def loadConfig():
	pass

class Config:
	hostname = 'extrastout.defiant.worf.co'
	token = '0ES'
	info = 'ExtraServ ~new~ IRC Services for Hybrid'

	@classmethod
	def password(cls, pw_name):
		with open('{1}/passwords/{0}.pw'.format(pw_name, cls.base_dir), 'r') as f:
			return f.readline().strip()
