RESET = "\033[39m"

def black(text):
	ret = []
	for line in text.splitlines():
		ret.append("\033[30m{0}{1}".format(line, RESET))
	return '\n'.join(ret)

def red(text):
	ret = []
	for line in text.splitlines():
		ret.append("\033[31m{0}{1}".format(line, RESET))
	return '\n'.join(ret)

def green(text):
	ret = []
	for line in text.splitlines():
		ret.append("\033[32m{0}{1}".format(line, RESET))
	return '\n'.join(ret)

def yellow(text):
	ret = []
	for line in text.splitlines():
		ret.append("\033[33m{0}{1}".format(line, RESET))
	return '\n'.join(ret)

def blue(text):
	ret = []
	for line in text.splitlines():
		ret.append("\033[34m{0}{1}".format(line, RESET))
	return '\n'.join(ret)

def magenta(text):
	ret = []
	for line in text.splitlines():
		ret.append("\033[35m{0}{1}".format(line, RESET))
	return '\n'.join(ret)

def cyan(text):
	ret = []
	for line in text.splitlines():
		ret.append("\033[36m{0}{1}".format(line, RESET))
	return '\n'.join(ret)

def light_gray(text):
	ret = []
	for line in text.splitlines():
		ret.append("\033[37m{0}{1}".format(line, RESET))
	return '\n'.join(ret)

def dark_gray(text):
	ret = []
	for line in text.splitlines():
		ret.append("\033[90m{0}{1}".format(line, RESET))
	return '\n'.join(ret)

def light_red(text):
	ret = []
	for line in text.splitlines():
		ret.append("\033[91m{0}{1}".format(line, RESET))
	return '\n'.join(ret)

def light_green(text):
	ret = []
	for line in text.splitlines():
		ret.append("\033[92m{0}{1}".format(line, RESET))
	return '\n'.join(ret)

def light_yellow(text):
	ret = []
	for line in text.splitlines():
		ret.append("\033[93m{0}{1}".format(line, RESET))
	return '\n'.join(ret)

def light_blue(text):
	ret = []
	for line in text.splitlines():
		ret.append("\033[94m{0}{1}".format(line, RESET))
	return '\n'.join(ret)

def light_magenta(text):
	ret = []
	for line in text.splitlines():
		ret.append("\033[95m{0}{1}".format(line, RESET))
	return '\n'.join(ret)

def light_cyan(text):
	ret = []
	for line in text.splitlines():
		ret.append("\033[96m{0}{1}".format(line, RESET))
	return '\n'.join(ret)

def white(text):
	ret = []
	for line in text.splitlines():
		ret.append("\033[97m{0}{1}".format(line, RESET))
	return '\n'.join(ret)
