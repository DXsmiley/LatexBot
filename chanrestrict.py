# Used to restrict the servers and channels that the bot may access.

# An empty whitelist assumes the bot may access everything that's not on the blacklist.
# Channel rules 'server#channel' override server rules 'server'.

white = []
black = []
private = True

def setup(whitelist, blacklist, allow_private = True):
	global white
	global black
	global private
	white = [i.strip().lower() for i in whitelist]
	black = [i.strip().lower() for i in blacklist]
	private = allow_private
	bset = set(blacklist)
	for i in white:
		if i in bset:
			raise ValueError('{} is in the blacklist and the whitelist'.format(i))

def check(message):
	allow = False
	if message.channel.is_private:
		allow = private
	else:
		ser = message.server.name.lower()
		chn = ser + '#' + message.channel.name.lower()
		if len(white) == 0:
			allow = True
		if ser in white:
			allow = True
		if ser in black:
			allow = False
		if chn in white:
			allow = True
		if chn in black:
			allow = False
	return allow

# This only works for the on_message function.
def apply(func):
	def on_message(message):
		if check(message):
			func(message)
	return on_message