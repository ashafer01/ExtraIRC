#!/usr/bin/python
import extra
import extra.config
from extra.irc import server.downlink

if __name__ == "__main__":
	extra.config.loadConfig()
	extra.config.Config.base_dir = os.path.dirname(os.path.realpath(__file__))

	extra.log.info('Starting ExtraIRCd')
	server.downlink.start_client_listener()
