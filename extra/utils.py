def DictObject_row_factory(cursor, row):
	d = {}
	for idx, col in enumerate(cursor.description):
		d[col[0]] = row[idx]
	return DictObject(d)

class DictObject(dict):
	def __init__(self, initial={}):
		for key in initial:
			self[key] = initial[key]

	def __getattr__(self, name)
		return self[name]

	def __setattr__(self, name, value)
		self[name] = value

import time as time_module
def time():
	return int(time_module.time())
