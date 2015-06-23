import re
import collections

def DictObject_row_factory(cursor, row):
	d = {}
	for idx, col in enumerate(cursor.description):
		d[col[0]] = row[idx]
	return DictObject(d)

class DictObject(dict):
	def __init__(self, initial={}):
		for key in initial:
			self[key] = initial[key]

	def __getattr__(self, name):
		return self[name]

	def __setattr__(self, name, value):
		self[name] = value

	def __str__(self):
		return 'DictObject({0})'.format(dict.__str__(self))

import time as time_module
def time():
	return int(time_module.time())

def str_split(text, length=1):
	return [ text[i:i+length] for i in range(0, len(text), length) ]

def smart_split(text, length=80):
	# text is already short enough
	if len(text) < length:
		return [text]

	# process text
	ret = []
	words = collections.deque(text.split())
	line = words.popleft()
	while len(words) > 0:
		if len(words[0]) > length:
			ret.append(words.popleft())
			continue
		if len(line) + len(words[0]) + 1 <= length:
			line += ' ' + words.popleft()
		else:
			ret.append(line)
			line = words.popleft()
	return ret
