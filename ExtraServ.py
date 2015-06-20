#!/usr/bin/python
import extra.irc
import extra.irc.network.twistedUplink

IRC_ENDPOINT_CLASS = extra.irc.Server

from twisted.internet import reactor
import sys

def start_twisted():
	reactor.connectTCP('localhost', 9999, extra.irc.twistedUplink.ServerUplinkFactory(ircEndpointClass=IRC_ENDPOINT_CLASS))
	reactor.run()

def start_stdin():
	while True:
		IRC_ENDPOINT_CLASS.handleLine(sys.stdin.readline())

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser(description='Start ExtraServ IRC Services for Hybrid')
	group = parser.add_mutually_exclusive_group()
	group.add_argument('--twisted', dest='run', action='store_const', const=start_twisted)
	group.add_argument('--stdin', dest='run', action='store_const', const=start_stdin)
	opts = parser.parse_args()

	opts.run()
