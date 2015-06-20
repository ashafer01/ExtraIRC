#!/usr/bin/python

if __name__ == '__main__':
	import argparse
	import extra.ircEndpoint
	import extra.handlers.ServiceHandler

	parser = argparse.ArgumentParser(description='Start ExtraServ IRC Services for Hybrid')
	group = parser.add_mutually_exclusive_group()
	group.add_argument('--twisted', dest='run', action='store_const', const=extra.ircEndpoint.start_twisted)
	group.add_argument('--stdio', dest='run', action='store_const', const=extra.ircEndpoint.start_stdio)
	opts = parser.parse_args()

	if opts.run is None:
		opts.run = extra.ircEndpoint.start_twisted

	opts.run(extra.handlers.ServiceHandler)
