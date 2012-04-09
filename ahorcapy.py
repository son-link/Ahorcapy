#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Ahorcapy r3
#  
#  Copyright 2012 Alfonso Saavedra "Son Link" <sonlink.dourden@gmail.com>
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

from re import search
from random import randint
import curses

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
height = 20 ; width = 40
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
		
		stdscr.addstr(1, 4, 'Ahorcapy. (c) 2011 Alfonso Saavedra "Son Link"' , curses.color_pair(3) )
		stdscr.addstr(3, 4, '_______')
		stdscr.addstr(4, 4, '/     |')
		stdscr.addstr(5, 4, '|')
		stdscr.addstr(6, 4, '|')
		stdscr.addstr(7, 4, '|')
		stdscr.addstr(8, 4, '|')
		stdscr.addstr(10, 4, 'Palabra: %s' % self.word2)
		stdscr.refresh()
		
		self.checkLetter()
	
	def checkLetter(self):
		"""
		Comprueba si la letra esta en la palabra.
		"""
		key = chr(stdscr.getch()).lower()
		#key.encode(code)

		if search('[a-z]$', key):
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
							
			else:
				curses.beep()
				self.errors += 1
			
			self.redraw()
		
		elif key == 27:
			# Si se pulsa la tecla Esc se cierra el juego
			self.salir()

	def redraw(self):
		"""
		Repinta la ventana
		"""
		letters = ''
				
		if self.word2 != self.word:
			
			if self.errors == 1:
				stdscr.addstr(5, 4, '|     O')
			
			if self.errors == 2:
				stdscr.addstr(6, 4, '|     |')
				
			if self.errors == 3:
				stdscr.addstr(6, 4, '|    /|')
				
			if self.errors == 4:
				stdscr.addstr(6, 4, '|    /|\\')
				
			if self.errors == 5:
				stdscr.addstr(7, 4, '|    /')
				
			if self.errors == 6:
				stdscr.addstr(7, 4, '|    / \\')
				stdscr.addstr(10, 4, 'Palabra: %s' % self.word2)
					
				stdscr.addstr(12, 4, '¡Has fallado!', curses.color_pair(1) )
				self.retry()
				
			stdscr.addstr(10, 4, 'Palabra: %s' % self.word2)
			
			for k in self.letters:
				letters += ' ' + k
				
			stdscr.addstr(14, 4, 'Letras introducidas hasta el momento:%s' % letters)
			stdscr.refresh()
			self.checkLetter()
		
		else:
			stdscr.addstr(10, 4, 'Palabra: %s' % self.word2)
			stdscr.addstr(12, 4, '¡Has ganado!', curses.color_pair(2) )
			
			self.retry()
	
	def retry(self):
		"""
		Al terminar la partida nos preguntara si queremos volver a jugar
		"""
		stdscr.addstr(16, 4, 'Desea jugar otra vez niño [S/n]')
		key = chr(stdscr.getch())
		
		if key == 's' or key == 'S':
			self.positions = []
			self.letters = []
			self.errors = 0
			stdscr.clear()
			
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
			
			stdscr.addstr(1, 4, 'Ahorcapy. (c) 2011 Alfonso Saavedra "Son Link"' , curses.color_pair(3) )
			stdscr.addstr(3, 4, '_______')
			stdscr.addstr(4, 4, '/     |')
			stdscr.addstr(5, 4, '|')
			stdscr.addstr(6, 4, '|')
			stdscr.addstr(7, 4, '|')
			stdscr.addstr(8, 4, '|')
			stdscr.addstr(10, 4, 'Palabra: %s' % self.word2)
			stdscr.refresh()			
			self.redraw()
			
		elif key == 'n' or key == 'N':
			self.salir()
			
	def salir(self):
		"""
		Salimos del programa
		"""
		curses.endwin()
		exit()
			
if __name__ == '__main__':
	Ahorcapy()
