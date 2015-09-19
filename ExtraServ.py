#!/usr/bin/python
import extra
import extra.irc.service
import extra.uplink
import extra.config

if __name__ == '__main__':
	import argparse
	import os
	parser = argparse.ArgumentParser(description='Start ExtraServ IRC Services for Hybrid')
	extra.uplink.setup_argparse_opts(parser)
	opts = parser.parse_args()

	if opts.run is None:
		opts.run = extra.uplink.start_twisted

	extra.config.loadConfig()
	extra.config.Config.base_dir = os.path.dirname(os.path.realpath(__file__))

	extra.log.info('Starting ExtraServ')
	opts.run(extra.irc.service)
