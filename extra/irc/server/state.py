import sqlite3
from extra import utils
from extra import log

class state(object):
	def __init__(self):
		self.dbc = sqlite3.connect(':memory:')
		self.dbc.row_factory = utils.DictObject_row_factory
		self.dbc.text_factory = str

		self.channels = channels(self.dbc)
		self.nicks = nicks(self.dbc)
		self.servers = servers(self.dbc)
		self.uplinkServer = None

	def changeNick(self, oldnick, newnick):
		self.nicks.change(oldnick, newnick)
		self.channels.changeNick(oldnick, newnick)

	def removeNick(self, nick):
		self.nicks.remove(nick)
		self.channels.removeNick(nick)

	def isNick(self, nick):
		return self.nicks.get(nick) is not None

	def isServer(self, server):
		return self.servers.get(server) is not None

	def isChannel(self, channel):
		return self.channels.get(channel) is not None

class servers(object):
	def __init__(self, dbc):
		self.dbc = dbc
		self.dbc.execute('CREATE TABLE IF NOT EXISTS servers (name varchar(100), token char(3), desc varchar(200))')
		self.dbc.commit()

	def get(self, server):
		c = self.dbc.execute('SELECT * FROM servers WHERE name=?', (server,))
		return c.fetchone()

	def add(self, **kwargs):
		if self.get(kwargs['name']) is None:
			self.dbc.execute('INSERT INTO servers (name, token, desc) VALUES (:name, :token, :desc)', kwargs)
			self.dbc.commit()
			log.info('Added server {name}'.format(**kwargs))
		else:
			raise Exception('Server already exists')

	def remove(self, server):
		c = self.dbc.execute('DELETE FROM servers WHERE name=?', (server,))
		n = c.rowcount
		self.dbc.commit()
		if n > 0:
			log.info('Removed server {0}'.format(server))
		else:
			log.notice('server {0} does not exist on remove'.format(server))

class nicks(object):
	def __init__(self, dbc):
		self.dbc = dbc
		self.dbc.execute('CREATE TABLE IF NOT EXISTS nicks (nick varchar(24), user varchar(72), host varchar(100), modes varchar(20), server varchar(100), realname varchar(100))')
		self.dbc.commit()

	def get(self, nick):
		nick = nick.lower()
		c = self.dbc.execute('SELECT * FROM nicks WHERE nick=?', (nick,))
		return c.fetchone()

	def getByUser(self, user):
		user = user.lower()
		c = self.dbc.execute('SELECT * FROM nicks WHERE user=?', (user,))
		return c.fetchone()

	def add(self, **kwargs):
		kwargs['nick'] = kwargs['nick'].lower()
		kwargs['user'] = kwargs['user'].lower()
		if self.get(kwargs['nick']) is None:
			self.dbc.execute('INSERT INTO nicks (nick,user,host,modes,server,realname) VALUES (:nick,:user,:host,:modes,:server,:realname)', kwargs)
			self.dbc.commit()
			log.info('Added nick {nick}'.format(**kwargs))
		else:
			raise Exception('nick already exists')

	def change(self, oldnick, newnick):
		oldnick = oldnick.lower()
		newnick = newnick.lower()
		c = self.dbc.execute('UPDATE nicks SET nick=? WHERE nick=?', (newnick, oldnick))
		n = c.rowcount
		self.dbc.commit()
		if n > 0:
			log.debug('Changed nick {0} to {1} in nick state'.format(oldnick, newnick))
		else:
			log.notice('Nick {0} does not exist on change'.format(oldnick))

	def remove(self, nick):
		nick = nick.lower()
		c = self.dbc.execute('DELETE FROM nicks WHERE nick=?', (nick,))
		n = c.rowcount
		self.dbc.commit()
		if n > 0:
			log.debug('Removed nick {0}'.format(nick))
		else:
			log.notice('Nick {0} does not exist on remove'.format(nick))

	def setModes(self, nick, modes):
		nick = nick.lower()
		if isinstance(modes, set):
			modes = ''.join(modes)
		c = self.dbc.execute('UPDATE nicks SET modes=? WHERE nick=?', (modes, nick))
		n = c.rowcount
		self.dbc.commit()
		if n > 0:
			log.debug('Updated modes for {0}'.format(nick))
		else:
			log.notice('Nick {0} does not exist on setModes'.format(nick))

class channels(object):
	def __init__(self, dbc):
		self.dbc = dbc
		self.dbc.execute('CREATE TABLE IF NOT EXISTS channels (channel varchar(60), modes varchar(40), mode_k varchar(72), mode_l varchar(6))')
		self.dbc.execute('CREATE TABLE IF NOT EXISTS channel_members (channel varchar(60), nick varchar(24))')
		self.dbc.execute('CREATE TABLE IF NOT EXISTS channel_modelists (channel varchar(60), mode char(1), value varchar(40))')
		self.dbc.commit()

	def get(self, channel):
		channel = channel.lower()
		c = self.dbc.execute('SELECT * FROM channels WHERE channel=?', (channel,))
		return c.fetchone()

	def getMembers(self, channel):
		channel = channel.lower()
		c = self.dbc.execute('SELECT nick FROM channel_members WHERE channel=?', (channel,))
		ret = []
		for row in c:
			ret.append(row.nick)
		return ret

	def getModelist(self, channel, modechar):
		channel = channel.lower()
		c = self.dbc.execute('SELECT value FROM channel_modelists WHERE channel=? AND mode=?', (channel, modechar))
		ret = []
		for row in c:
			ret.append(row.value)
		return ret

	def addToModelist(self, channel, mode, value):
		channel = channel.lower()
		current_list = self.getModelist(channel, mode)
		if value not in current_list:
			self.dbc.execute('INSERT INTO channel_modelists (channel, mode, value) VALUES (?, ?, ?)', (channel, mode, value))
			self.dbc.commit()
			log.debug('Added {0} to modelist {1} for {2}'.format(value, mode, channel))
		else:
			log.debug('{0} already on modelist {1} for {2}'.format(value, mode, channel))

	def removeFromModelist(self, channel, mode, value):
		channel = channel.lower()
		c = self.dbc.execute("DELETE FROM channel_modelists WHERE channel=? AND mode=? AND value=?", (channel, mode, member))
		n = c.rowcount
		if n > 0:
			log.debug('Removed {0} from modelist {1} for {2}'.format(value, mode, channel))
		else:
			log.debug('No changes made on removeFromModelist')

	def add(self, **kwargs):
		kwargs['channel'] = kwargs['channel'].lower()
		if self.get(kwargs['channel']) is None:
			self.dbc.execute('INSERT INTO channels (channel, modes, mode_k, mode_l) VALUES (:channel, :modes, :mode_k, :mode_l)', kwargs)
			self.dbc.commit()
			log.debug("Added new channel {0}".format(kwargs['channel']))
			log.debug1("New channel parameters: {0}".format(kwargs))
		else:
			log.notice("Channel {0} already exists when adding new channel".format(kwargs['channel']))

	def addMember(self, channel, nick):
		channel = channel.lower()
		nick = nick.lower()
		if nick not in self.getMembers(channel):
			self.dbc.execute('INSERT INTO channel_members (channel, nick) VALUES (?, ?)', (channel, nick))
			self.dbc.commit()
			log.debug("Added {0} to {1}".format(nick, channel))
		else:
			log.debug("{0} is already a member of channel {1}".format(nick, channel))

	def removeMember(self, channel, member):
		channel = channel.lower()
		member = member.lower()
		n = 0
		c = self.dbc.execute("DELETE FROM channel_members WHERE channel=? AND nick=?", (channel, member))
		n += c.rowcount
		c = self.dbc.execute("DELETE FROM channel_modelists WHERE channel=? AND mode IN('o','h','v') AND value=?", (channel, member))
		n += c.rowcount
		self.dbc.commit()
		if n > 0:
			log.debug1("Removed {0} from {1}".format(member, channel))
		else:
			log.debug("Member {0} not in {1} on removeMember".format(member, channel))

	def changeNick(self, oldnick, newnick):
		oldnick = oldnick.lower()
		newnick = newnick.lower()
		n = 0
		c = self.dbc.execute("UPDATE channel_members SET nick=? WHERE nick=?", (newnick, oldnick))
		n += c.rowcount
		c = self.dbc.execute("UPDATE channel_modelists SET value=? WHERE mode IN('o','h','v') AND value=?", (newnick, oldnick))
		n += c.rowcount
		self.dbc.commit()
		if n > 0:
			log.info("Changed nick {0} => {1} in channel state".format(oldnick, newnick))
		else:
			log.notice("No changes made on changeNick for {0}".format(oldnick))

	def setModes(self, **params):
		params['channel'] = params['channel'].lower()
		query = 'UPDATE channels SET modes=:modes'
		if 'mode_k' in params and params['mode_k'] is not None:
			query += ', mode_k=:mode_k'
		if 'mode_l' in params and params['mode_l'] is not None:
			query += ', mode_l=:mode_l'
		query += ' WHERE channel=:channel'
		if isinstance(params['modes'], set):
			params['modes'] = ''.join(params['modes'])
		c = self.dbc.execute(query, params)
		n = c.rowcount
		self.dbc.commit()
		if n > 0:
			log.info("Updated modes for channel {0} -> {1}".format(params['channel'], params))
		else:
			log.notice("No changes made on setModes for {0}".format(params['channel']))

	def removeNick(self, nick):
		nick = nick.lower()
		n = 0
		c = self.dbc.execute("DELETE FROM channel_members WHERE nick=?", (nick,))
		n += c.rowcount
		c = self.dbc.execute("DELETE FROM channel_modelists WHERE mode IN('o','h','v') AND value=?", (nick,))
		n += c.rowcount
		self.dbc.commit()
		if n > 0:
			log.info("Removed nick {0} from channel state".format(nick))
		else:
			log.debug("No changes made on removeNick for {0}".format(nick))

	def getNickChannels(self, nick):
		nick = nick.lower()
		c = self.dbc.execute("SELECT channel FROM channel_members WHERE nick=?", (nick,))
		ret = []
		for row in c:
			ret.append(row.channel)
		return set(ret)

