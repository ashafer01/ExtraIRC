#!/usr/bin/python
import extra
from extra.uplink import twistedUplink, stdioUplink
import extra.irc.service

if __name__ == '__main__':
	import argparse
	import os
	parser = argparse.ArgumentParser(description='Start ExtraServ IRC Services for Hybrid')
	group = parser.add_mutually_exclusive_group()
	group.add_argument('--twisted',
		dest='run',
		action='store_const',
		const=twistedUplink.start,
		help='Use twisted to connect to the uplink server (default)'
	)
	group.add_argument('--stdio',
		dest='run',
		action='store_const',
		const=stdioUplink.start,
		help='Accept IRC commands on stdin and reply on stdout'
	)
	opts = parser.parse_args()

	if opts.run is None:
		opts.run = twistedUplink.start

	extra.config.loadConfig()
	extra.config.Config.base_dir = os.path.dirname(os.path.realpath(__file__))

	extra.log.info('Starting ExtraServ')
	opts.run(extra.irc.service)
