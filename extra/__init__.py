import log
from config import Config

config = Config()

def log_incoming(line):
	log.info(log.color.cyan("<= " + line))

def log_outgoing(line):
	log.info(log.color.green("=> " + line))

