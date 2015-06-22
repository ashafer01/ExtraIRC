import TerminalColor as color
import datetime

FATAL = 0
ERROR = 1
WARNING = 2
NOTICE = 3
INFO = 4
DEBUG = 5
DEBUG1 = 6
DEBUG2 = 7
DEBUG3 = 8

LEVEL = DEBUG3

def level_to_string(level):
	if level == FATAL:
		return 'FATAL'
	if level == ERROR:
		return 'ERROR'
	if level == WARNING:
		return 'WARNING'
	if level == NOTICE:
		return 'NOTICE'
	if level == INFO:
		return 'INFO'
	if level == DEBUG:
		return 'DEBUG'
	if level == DEBUG1:
		return 'DEBUG1'
	if level == DEBUG2:
		return 'DEBUG2'
	if level == DEBUG3:
		return 'DEBUG3'

def timestamp():
	return datetime.datetime.utcnow().strftime('%a %Y-%m-%d %H:%M:%S.%f')

def do_message(level, message):
	if level <= LEVEL:
		for line in message.split('\n'):
			print '[{0}] {1}: {2}'.format(timestamp(), level_to_string(level), line)

def fatal(message):
	do_message(FATAL, color.light_red(message))
def error(message):
	do_message(ERROR, color.red(message))
def warning(message):
	do_message(WARNING, color.yellow(message))
def notice(message):
	do_message(NOTICE, message)
def info(message):
	do_message(INFO, message)
def debug(message):
	do_message(DEBUG, color.light_gray(message))
def debug1(message):
	do_message(DEBUG1, color.dark_gray(message))
def debug2(message):
	do_message(DEBUG2, color.dark_gray(message))
def debug3(message):
	do_message(DEBUG3, color.dark_gray(message))
