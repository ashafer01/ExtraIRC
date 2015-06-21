#!/usr/bin/python
import extra
import extra.service
import extra.config

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser(description='Start ExtraServ IRC Services for Hybrid')
	group = parser.add_mutually_exclusive_group()
	group.add_argument('--twisted', dest='run', action='store_const', const=extra.start_twisted)
	group.add_argument('--stdio', dest='run', action='store_const', const=extra.start_stdio)
	opts = parser.parse_args()

	if opts.run is None:
		opts.run = extra.start_twisted

	extra.config.loadConfig()
	opts.run(extra.service.handler)
