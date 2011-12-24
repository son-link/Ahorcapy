#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  ahorcapy.py
#  
#  Copyright 2011 Alfonso Saavedra "Son Link" <sonlink.dourden@gmail.com>
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
# (c) 2011 Alfonso Saavedra "Son Link"

from os import system
from re import search, UNICODE
from random import randint
from termcolor import colored

class Ahorcapy():
	
	def __init__(self):
		
		self.positions = []
		self.letters = []
		self.errors = 0
		
		f = open('words.txt', 'r')
		words = f.readlines()
		f.close()
		
		n = randint(0, len(words)-1)
		self.word = words[n].split()[0]
		
		self.word2 = ''
		
		i = 0
		while i <= len(self.word):
			self.word2 += '_'
			i += 1
		
		self.interface = [
		'\tAhorcapy. (c) 2011 Alfonso Saavedra "Son Link"\n',
		'\t_______',
		'\t/     |',
		'\t|',
		'\t|',
		'\t|',
		'\t|\n',
		'\tPalabra:%s\n' % self.word2,
		'\tLetras introducidas hasta el momento:\n']
		
		self.redraw()
		
	def checkLetter(self, key):
				
		if search('[A-Za-z]$', key):
			
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
					self.beep()
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
				self.beep()
				self.errors += 1
			
		self.redraw()

	def redraw(self):
		system("clear")
		letters = ''
				
		if self.word2 != self.word:
			
			if self.errors == 1:
				self.interface[3] = '\t|     O'
			
			if self.errors == 2:
				self.interface[4] = '\t|     |'
				
			if self.errors == 3:
				self.interface[4] = '\t|    /|'
				
			if self.errors == 4:
				self.interface[4] = '\t|    /|\\'
				
			if self.errors == 5:
				self.interface[5] = '\t|    /'
				
			if self.errors == 6:
				self.interface[5] = '\t|    / \\'
				self.interface[7] = '\tPalabra: %s\n' % self.word2
				for line in self.interface:
					print colored(line, 'red', attrs=['bold'])
					
				print colored('\t¡HAS FALLADO!', 'red', attrs=['bold', 'blink'])
				self.retry()
				
			self.interface[7] = '\tPalabra: %s\n' % self.word2
			
			for k in self.letters:
				letters += ' ' + k
				
			self.interface[8] = '\tLetras introducidas hasta el momento:%s\n' % letters
			
			for line in self.interface:
				print colored(line, 'white', attrs=['bold'])
			
			key = raw_input('\tEscriba una letra: ')
			
			self.checkLetter(key)
		
		else:
			self.interface[7] = '\tPalabra: %s\n' % self.word2			
			for line in self.interface:
				print colored(line, 'white', attrs=['bold'])
			
			print colored('\t¡HAS GANADO!', 'green', attrs=['bold','blink'])
			
			self.retry()
			
	def beep(self):
		f=open('/dev/tty','w')
		f.write(chr(7))
		f.close()
		
	
	def retry(self):
		
		q = raw_input('\tComenzar otra partida [s/N]: ')
		
		if q == 's' or q == 'S':
			self.positions = []
			self.letters = []
			self.errors = 0
			
			f = open('words.txt', 'r')
			words = f.readlines()
			f.close()
			
			n = randint(0, len(words)-1)
			self.word = words[n].split()[0]
			
			self.word2 = ''
			
			i = 0
			while i <= len(self.word):
				self.word2 += '_'
				i += 1
			
			self.interface = [
			'\tAhorcapy. (c) 2011 Alfonso Saavedra "Son Link"\n',
			'\t_______',
			'\t/     |',
			'\t|',
			'\t|',
			'\t|',
			'\t|\n',
			'\tPalabra:%s\n' % self.word2,
			'\tLetras introducidas hasta el momento:\n']
			
			self.redraw()
			
		elif q == 'n' or q == 'N' or not q:
			exit()
			
		else:
			self.redraw()
			
if __name__ == '__main__':
	Ahorcapy()
