#!/usr/bin/python
import extra
import extra.config
import extra.irc.server
from extra.downlink import twistedDownlink

if __name__ == "__main__":
	extra.config.loadConfig()
	extra.config.Config.base_dir = os.path.dirname(os.path.realpath(__file__))

	extra.log.info('Starting ExtraIRCd')
	twistedDownlink.start(extra.irc.server)
