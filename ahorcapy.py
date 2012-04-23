#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Ahorcapy r9
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
# (c) 2011-2012 Alfonso Saavedra "Son Link"
# http://sonlinkblog.blogspot.com

import curses, curses.panel, gettext

from random import randint
from optparse import OptionParser
#from os.path import isfile, isdir
from os import environ
from os import access, path, R_OK

APP = 'ahorcapy'
gettext.textdomain (APP)
gettext.bindtextdomain (APP, 'lang')
_ = gettext.gettext
gettext.install(APP, 'lang')

# Iniciamos Curses
stdscr = curses.initscr()
curses.start_color()
# Definimos los pares de color que usaremos
curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)
curses.noecho()
curses.cbreak()

# Configuramos e iniciamos la ventana del juego
begin_x = 1 ; begin_y = 1
height = 20 ; width = 20
win = curses.newwin(height, width, begin_y, begin_x)

class Ahorcapy():
	
	def __init__(self):
		"""
		Iniciamos el juego
		"""
		
		self.positions = []
		self.letters = []
		self.errors = 0
		
		f = open('words.txt', 'r')
		words = f.readlines()
		f.close()
		
		n = randint(0, len(words)-1)
		self.word = words[n].split()[0]
		
		self.word2 = ''
		
		i = 1
		while i <= len(self.word):
			self.word2 += '_'
			i += 1
		
		stdscr.addstr(1, 4, ' ______')
		stdscr.addstr(2, 4, '/     |')
		stdscr.addstr(3, 4, '|')
		stdscr.addstr(4, 4, '|')
		stdscr.addstr(5, 4, '|')
		stdscr.addstr(6, 4, '|')
		stdscr.addstr(9, 4, 'Palabra: %s' % self.word2)

		
		panel = self.show_letters()
		panel.show()
		curses.panel.update_panels()
		stdscr.refresh()
		
		self.checkLetter()
	
	def checkLetter(self):
		"""
		Comprueba si la letra esta en la palabra.
		"""
		k = stdscr.getch()
		
		if k >= 97 and k <= 122 or k >= 65 and k <= 90:
			key = chr(k).lower()
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
					curses.beep()
					self.errors += 1
							
				i = 0
				word2 = ''
				while i < len(self.word):
					if i in self.positions:
						word2 += self.word[i]
					else:
						word2 += '_'
					i += 1
					
				self.word2 = word2
			
			self.redraw()
		
		elif k == 27:
			# Si se pulsa la tecla Esc se cierra el juego
			self.salir()
		else:
			self.redraw()

	def redraw(self):
		"""
		Repinta la ventana
		"""
		letters = ''
				
		if self.word2 != self.word:
			
			if self.errors == 1:
				stdscr.addstr(3, 10, 'O')
			
			if self.errors == 2:
				stdscr.addstr(4, 10, '|')
				
			if self.errors == 3:
				stdscr.addstr(4, 9, '/|')
				
			if self.errors == 4:
				stdscr.addstr(4, 9, '/|\\')
				
			if self.errors == 5:
				stdscr.addstr(5, 9, '/')
				
			if self.errors == 6:
				stdscr.addstr(5, 9, '/ \\')
				stdscr.addstr(9, 4, _('Word: %s') % self.word)
					
				stdscr.addstr(11, 4, _('YOU FAIL!'), curses.color_pair(1) )
				self.retry()
				
			stdscr.addstr(9, 4, _('Word: %s') % self.word2)
			
			for k in self.letters:
				letters += ' ' + k
			
			panel = self.show_letters()
			panel.show()
			self.checkLetter()
		
		else:
			stdscr.addstr(9, 4, _('Word: %s') % self.word2)
			stdscr.addstr(11, 4, _('YOU WIN!'), curses.color_pair(2) )
			self.retry()
	
	def retry(self):
		"""
		Al terminar la partida nos preguntara si queremos volver a jugar
		"""
		stdscr.addstr(16, 4, _('Press any key to start new game or press ESC to exit'))
		key = stdscr.getch()
		
		if key < 256:
			if key == 27:
				self.salir()
			else:
				self.positions = []
				self.letters = []
				self.errors = 0
				stdscr.clear()
				self.show_letters(True)
				
				f = open('words.txt', 'r')
				words = f.readlines()
				f.close()
				
				n = randint(0, len(words)-1)
				self.word = words[n].split()[0]
				
				self.word2 = ''
				
				i = 1
				while i <= len(self.word):
					self.word2 += '_'
					i += 1
				
				stdscr.addstr(1, 4, ' ______')
				stdscr.addstr(2, 4, '/     |')
				stdscr.addstr(3, 4, '|')
				stdscr.addstr(4, 4, '|')
				stdscr.addstr(5, 4, '|')
				stdscr.addstr(6, 4, '|')
				stdscr.addstr(9, 4, 'Palabra: ______')
				
				stdscr.addstr(12, 4, 'Pulsa una tecla para iniciar una nueva partida')
				panel = self.show_letters()
				panel.show()
				self.redraw()
		else:
			self.retry()
			
	def show_letters(self, clear=False):
		letters = ''
		win = curses.newwin(6, 14, 1, 20)

		if clear:
			win.clear()
			
		
		win.addstr(0, 0, _('Letters:'))
		for l in self.letters:
				letters += l + ' '
		
		win.addstr(1, 0, letters)
		win.bkgdset(ord(' '), curses.color_pair(0))
		win.refresh()
		
		pan = curses.panel.new_panel(win)
		return pan
		
	def salir(self):
		"""
		Salimos del programa
		"""
		curses.endwin()
		exit()
			
if __name__ == '__main__':
	try:
		Ahorcapy()
	except KeyboardInterrupt:
		curses.endwin()
		exit()
