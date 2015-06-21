import sqlite3
import utils
import log

class state:
	def __init__(self):
		self.dbc = sqlite3.connect(':memory:')
		self.dbc.row_factory = utils.DictObject_row_factory

		self.channels = channels(self.dbc)
		self.nicks = nicks(self.dbc)

	def changeNick(self, oldnick, newnick):
		self.nicks.change(oldnick, newnick)
		self.channels.changeNick(oldnick, newnick)

	def removeNick(self, nick):
		self.nicks.remove(nick)
		self.channels.removeNick(nick)

class nicks:
	def __init__(self, dbc):
		self.dbc = dbc
		db = self.dbc.cursor()
		db.execute('CREATE TABLE nicks (nick varchar(24), user varchar(72), host varchar(100), modes varchar(20), server varchar(100), realname varchar(100))')
		self.dbc.commit()

	def get(self, nick):
		c = self.dbc.cursor()
		c.execute('SELECT * FROM nicks WHERE nick=?', (nick,))
		return c.fetchone()

	def getByUser(self, user):
		c = self.dbc.cursor()
		c.execute('SELECT * FROM nicks WHERE user=?', (user,))
		return c.fetchone()

	def add(self, **kwargs):
		if self.get(kwargs['nick']) is None and self.getByuser(kwargs['user']):
			c = self.dbc.cursor()
			c.execute('INSERT INTO nicks (nick,user,host,modes,server,realname) VALUES (:nick,:user,:host,:modes,:server,:realname)', kwargs)
			self.dbc.commit()
		else:
			raise Exception('nick or user already exists')

	def change(self, oldnick, newnick):
		c = self.dbc.cursor()
		c.execute('UPDATE nicks SET nick=? WHERE nick=?', (newnick, oldnick))
		n = c.rowcount
		self.dbc.commit()
		if n > 0:
			log.debug('Changed nick {0} to {1} in nick state'.format(oldnick, newnick))
		else:
			log.notice('Nick {0} does not exist on change'.format(oldnick))

	def remove(self, nick):
		c = self.dbc.cursor()
		c.execute('DELETE FROM nicks WHERE nick=?', (nick,))
		n = c.rowcount
		self.dbc.commit()
		if n > 0:
			log.debug('Removed nick {0}'.format(nick))
		else:
			log.notice('Nick {0} does not exist on remove'.format(nick))

class channels:
	def __init__(self, dbc):
		self.dbc = dbc
		db = self.dbc.cursor()
		db.execute('CREATE TABLE channels (channel varchar(60), modes varchar(40), mode_k varchar(72), mode_l varchar(6))')
		db.execute('CREATE TABLE channel_members (channel varchar(60), nick varchar(24))')
		db.execute('CREATE TABLE channel_modelists (channel varchar(60), mode char(1), value varchar(40))')
		self.dbc.commit()

	def get(self, channel):
		c = self.dbc.cursor()
		c.execute('SELECT * FROM channels WHERE channel=?', (channel,))
		return c.fetchone()

	def getMembers(self, channel):
		c = self.dbc.cursor()
		c.execute('SELECT nick FROM channel_members WHERE channel=?', (channel,))
		ret = []
		for row in c:
			ret.append(c.nick)
		return ret

	def getModelist(self, channel, modechar):
		c = self.dbc.cursor()
		c.execute('SELECT value FROM channel_modelists WHERE channel=? AND mode=?', (channel, modechar))
		ret = []
		for row in c:
			ret.append(c.value)
		return ret

	def add(self, **kwargs):
		if self.getChannel(kwargs['channel']) is None:
			c = self.dbc.cursor()
			c.execute('INSERT INTO channels (channel, modes, mode_k, mode_l) VALUES (:channel, :modes, :mode_k, :mode_l)', kwargs)
			self.dbc.commit()
			log.debug("Added new channel {0}".format(kwargs['channel']))
			log.debug1("New channel parameters: {0}".format(kwargs))
		else:
			log.notice("Channel {0} already exists when adding new channel".format(kwargs['channel']))

	def addMember(self, channel, member):
		c = self.dbc.cursor()
		if member not in self.getChannelMembers(channel):
			c.execute('INSERT INTO channel_members (channel, nick, chanmodes) VALUES (?, ?, '')', (channel, member))
		else:
			log.debug1("{0} is already a member of channel {1}".format(member, channel))
		self.dbc.commit()
		log.debug("Added {0} to {1}".format(member, channel))

	def removeMember(self, channel, member):
		c = self.dbc.cursor()
		n = 0
		c.execute("DELETE FROM channel_members WHERE channel=? AND nick=?", (channel, member))
		n += c.rowcount
		c.execute("DELETE FROM channel_modelists WHERE channel=? AND mode IN('o','h','v') AND value=?", (channel, member))
		n += c.rowcount
		self.dbc.commit()
		if n > 0:
			log.debug("Removed {0} from {1}".format(member, channel))
		else:
			log.debug1("Member {0} not in {1} on removeMember".format(member, channel))

	def changeNick(self, oldnick, newnick):
		c = self.dbc.cursor()
		n = 0
		c.execute("UPDATE channel_members SET nick=? WHERE nick=?", (newnick, oldnick))
		n += c.rowcount
		c.execute("UPDATE channel_modelists SET value=? WHERE mode IN('o','h','v') AND value=?", (newnick, oldnick))
		n += c.rowcount
		self.dbc.commit()
		if n > 0:
			log.debug("Changed nick {0} => {1} in channel state".format(oldnick, newnick))
		else:
			log.notice("No changes made on changeNick for {0}".format(oldnick))

	def removeNick(self, nick):
		c = self.dbc.cursor()
		n = 0
		c.execute("DELETE FROM channel_members WHERE nick=?", (channel, member))
		n += c.rowcount
		c.execute("DELETE FROM channel_modelists WHERE mode IN('o','h','v') AND value=?", (channel, member))
		n += c.rowcount
		self.dbc.commit()
		if n > 0:
			log.debug("Removed nick {0} from channel state".format(nick))
		else:
			log.debug1("No changes made on removeNick for {0}".format(nick))

