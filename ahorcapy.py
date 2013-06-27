#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Ahorcapy r12 (0.9.2)
#
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#

# Versión del juego del ahorcado.
# (c) 2011-2013 Alfonso Saavedra "Son Link"
# http://sonlinkblog.blogspot.com/p/ahorcapy.html

import urwid, gettext, locale, glob

from random import choice
from sys import argv
from os.path import basename, splitext, isfile, isdir
from os import access, R_OK
from re import match

locale.setlocale(locale.LC_ALL, '')
APP = 'ahorcapy'
gettext.textdomain (APP)
gettext.bindtextdomain (APP, 'lang')
_ = gettext.gettext
gettext.install(APP, 'lang')

palette = [
    ('title', 'white', 'dark red'),
    ('game_over', 'light red', ''),
    ('winner', 'light green', '')]

class Ahorcapy():

	def __init__(self):
		"""
		Iniciamos el juego
		"""

		self.words = []
		self.words_position = -1
		listbuttons = []

		if len(argv) == 2:
			if not isfile(argv[1]) or not access(argv[1], R_OK):
				print (_('The file %s don\'t exists or you not have read permissions') % self.wordslist)
				exit(-1)
			else:
				self.on_file_select(None, argv[1])
		else:
			for f in glob.glob('lists/*.txt'):
				if isfile(f) and access(f, R_OK):
					filename = splitext(basename(f))[0]
					listbuttons.append(urwid.Button(filename, self.on_file_select, f))

		title = urwid.Text('Ahorcapy', align='center')
		map1 = urwid.AttrWrap(title, 'title')
		title_fill = urwid.Padding(map1, align='center')

		self.game = urwid.Text('')
		self.letters_insert = urwid.Text(u'')
		self.word_show = urwid.Text(u'')

		listbox_text = urwid.Text(_('Select a words list:'))
		listbox = urwid.ListBox(listbuttons)
		listbox = urwid.BoxAdapter(listbox, 7)
		listbox = urwid.Pile([listbox])

		self.status_text = urwid.Text('')
		self.box = urwid.Pile([title_fill, listbox_text, listbox, self.word_show, self.status_text])
		box2 = urwid.Padding(self.box, align='center', width=('relative', 50), min_width=60)
		box3 = urwid.Filler(box2, height='pack')
		loop = urwid.MainLoop(box3, palette, unhandled_input=self.key_pressed)
		loop.run()

	def on_file_select(self, w, filename):
		f = open(filename)
		words = f.readlines()
		for i in range(len(words)):
			element = choice(words)
			words.remove(element)
			self.words.append(element.strip())
		f.close()
		cols = urwid.Columns([self.game, self.letters_insert])
		self.box.widget_list.pop(1)
		self.box.widget_list[1] = cols
		self.reset_game()

	def key_pressed(self, key):
		if key == 'esc':
			raise urwid.ExitMainLoop()
		elif type(key).__name__ in ['str', 'unicode'] and len(key) == 1 and match(u'([a-zñ])', key.lower()) and not self.if_yesno:
			key = key.lower()

			if not key in self.letters:
				self.letters.append(key)
				self.letters.sort()

				if key in self.word:
					i = -1
					try:
						while 1:
							i = self.word.index(key, i+1)
							self.positions.append(i)
							self.positions.sort()
					except ValueError:
						pass
				else:
					self.errors += 1

				i = 0
				word2 = ''
				while i < len(self.word):
					if i in self.positions:
						word2 += self.word[i]
					else:
						word2 += '*'
					i += 1

				self.word2 = word2
				self.word_show.set_text(_('Word: %s') % self.word2)
			self.redraw()

	def redraw(self):
		"""
		Repinta la ventana
		"""
		letters = ''

		if self.word2 != self.word:

			if self.errors == 1:
				self.monigote[2] = '|     O'

			if self.errors == 2:
				self.monigote[3] =  '|     |'

			if self.errors == 3:
				self.monigote[3] = '|    /|'

			if self.errors == 4:
				self.monigote[3] = '|    /|\\'

			if self.errors == 5:
				self.monigote[4] = '|    /'

			if self.errors == 6:
				self.word_show.set_text(('game_over', _('Word: %s') % self.word))
				self.monigote[4] = '|    / \\'
				self.status_text.set_text(('game_over',  _('YOU FAIL!')))
				self.retry()

			for l in self.letters:
				letters += l + ' '

			self.letters_insert.set_text(letters)

			monigote = ''
			for m in self.monigote:
				monigote += m+'\n'
			if self.errors == 6:
				self.game.set_text(('game_over', monigote))
			else:
				self.game.set_text(monigote)

		else:
			self.word_show.set_text(_('Word: %s') % self.word2)
			self.status_text.set_text(('winner', _('YOU WIN!')))
			self.retry()

	def retry(self):
		self.if_yesno = True
		txt = urwid.Text(_('Try another word?'))
		yes = urwid.Button(_('Yes'), self.reset_game)
		no = urwid.Button(_('No'), self.salir)

		confirm_buttons = urwid.GridFlow([yes, no], 8, 3, 0, 'right')
		box = urwid.Columns([txt, confirm_buttons])
		self.box.widget_list.append(box)
		self.box.set_focus(4)

	def reset_game(self, *args):
		"""
		Reseteamos el juego o lo mostramos por primera vez
		"""
		self.words_position += 1
		self.letters = []
		self.positions = []
		self.if_yesno = False
		self.box.set_focus(1)
		self.errors = 0
		self.word = ''
		self.letters_insert.set_text('')
		self.word_show.set_text('')
		self.status_text.set_text('')

		if len(self.box.widget_list) == 5:
			self.box.widget_list.pop(4)
			self.box.set_focus(1)

		self.monigote = [' ______', '/     |', '|', '|', '|', '|']

		monigote = ''
		for m in self.monigote:
			monigote += m+'\n'

		self.game.set_text(monigote)

		self.word = self.words[self.words_position]

		self.word2 = ''

		i = 1
		while i <= len(self.word):
			self.word2 += '*'
			i += 1

		self.word_show.set_text(_('Word: %s') % self.word2)

	def salir(self, *args):
		"""
		Salimos del programa
		"""
		raise urwid.ExitMainLoop()

if __name__ == '__main__':
	try:
		Ahorcapy()
	except KeyboardInterrupt:
		exit()
