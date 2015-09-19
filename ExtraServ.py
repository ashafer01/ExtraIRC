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
		dest='startUplink',
		action='store_const',
		const=twistedUplink.start,
		help='Use twisted to connect to the uplink server (default)'
	)
	group.add_argument('--stdio',
		dest='startUplink',
		action='store_const',
		const=stdioUplink.start,
		help='Accept IRC commands on stdin and reply on stdout'
	)
	opts = parser.parse_args()

	if opts.startUplink is None:
		opts.startUplink = twistedUplink.start

	extra.config.base_dir = os.path.dirname(os.path.realpath(__file__))

	extra.log.info('Starting ExtraServ')
	opts.startUplink(extra.irc.service)
