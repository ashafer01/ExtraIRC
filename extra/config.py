def loadConfig():
	pass

class Config:
	hostname = 'extrastout.defiant.worf.co'
	token = '0ES'
	info = 'ExtraServ ~new~ IRC Services for Hybrid'

	@staticmethod
	def password(pw_name):
		with open('password/{0}.pw'.format(pw_name), 'r') as f:
			return f.readline().strip()
