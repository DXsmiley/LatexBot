import discord
import urllib.request
import random
import os
import json
import shutil
import asyncio
import sys

import chanrestrict

LATEX_TEMPLATE="template.tex"

HELP_MESSAGE = r"""
Hello! I'm the *LaTeX* math bot!

You can type mathematical *LaTeX* into the chat and I'll automatically render it!

Simply use the `!tex` command.

**Examples**

`!tex x = 7`

`!tex \sqrt{a^2 + b^2} = c`

`!tex \int_0^{2\pi} \sin{(4\theta)} \mathrm{d}\theta`

**Notes**

Using the `\begin` or `\end` in the *LaTeX* will probably result in something failing.

"""

class LatexBot(discord.Client):
	#TODO: Check for bad token or login credentials using try catch
	def __init__(self):
		super().__init__()

		self.checkForConfig()
		self.settings = json.loads(open('settings.json').read())

		# Quick and dirty defaults of colour settings, if not already present in the settings
		if 'latex' not in self.settings:
			self.settings['latex'] = {
							'background-colour': '36393E',
							'text-colour': 'DBDBDB'
			}

		chanrestrict.setup(self.settings['channels']['whitelist'],
					       self.settings['channels']['blacklist'])

		#Check if user is using a token or login
		if self.settings['login_method'] == 'token':
			self.run(self.settings['login']['token'])
		elif self.settings['login_method'] == 'account':
			self.login(settings['login']['email'], settings['login']['password'])
			self.run()
		else:
			raise Exception('Bad config: "login_method" should set to "login" or "token"')

	#Check that config exists
	def checkForConfig(self):
		if not os.path.isfile('settings.json'):
			shutil.copyfile('settings_default.json', 'settings.json')
			print('Now you can go and edit `settings.json`.')
			print('See README.md for more information on these settings.')


	def vprint(self, *args, **kwargs):
		if self.settings.get('verbose', False):
			print(*args, **kwargs)

	#Outputs bot info to user
	@asyncio.coroutine
	def on_ready(self):
		print('------')
		print('Logged in as')
		print(self.user.name)
		print(self.user.id)
		print('------')

	async def on_message(self, message):
		if chanrestrict.check(message):

			msg = message.content

			for c in self.settings['commands']['render']:
				if msg.startswith(c):
					latex = msg[len(c):].strip()
					self.vprint('Latex:', latex)

					if self.settings['renderer'] == 'external':
						fn = self.generate_image_online(latex)
					if self.settings['renderer'] == 'local':
						fn = self.generate_image(latex)
						# raise Exception('TODO: Renable local generation')

					if os.path.getsize(fn) > 0:
						await self.send_file(message.channel, fn)
						self.vprint('Success!')
					else:
						await self.send_message(message.channel, 'Something broke. Check the syntax of your message. :frowning:')
						self.vprint('Failure.')

					break

			if msg in self.settings['commands']['help']:
				self.vprint('Showing help')
				await self.send_message(message.author, HELP_MESSAGE)

	# Generate LaTeX locally. Is there such things as rogue LaTeX code?
	def generate_image(self, latex):
		num = str(random.randint(0, 2 ** 31))
		latex_file = num + '.tex'
		dvi_file = num + '.dvi'
		with open(LATEX_TEMPLATE, 'r') as textemplatefile:
			textemplate = textemplatefile.read()

			with open(latex_file, 'w') as tex:
				backgroundcolour = self.settings['latex']['background-colour']
				textcolour = self.settings['latex']['text-colour']
				latex = textemplate.replace('__DATA__', latex).replace('__BACKGROUNDCOLOUR__', backgroundcolour).replace('__TEXTCOLOUR__', textcolour)

				tex.write(latex)
				tex.flush()
				tex.close()
		os.system('latex -quiet ' + latex_file)
		os.system('dvipng -q* -D 300 -T tight ' + dvi_file)
		png_file = num + '1.png'
		return png_file

	# More unpredictable, but probably safer for my computer.
	def generate_image_online(self, latex):
		url = 'http://frog.isima.fr/cgi-bin/bruno/tex2png--10.cgi?'
		url += urllib.parse.quote(latex, safe='')
		fn = str(random.randint(0, 2 ** 31)) + '.png'
		urllib.request.urlretrieve(url, fn)
		return fn

if __name__ == "__main__":
	LatexBot()
