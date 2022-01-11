#!/usr/bin/python3

import io
import os
import sys
import math
import time
import json
import pygame
import requests
import argparse
import pygame.locals
from io import BytesIO
from PIL import Image


# --- Variables -----------------------------------------------------------------------------------

pygame.init()
version = '0.01'	# init
font09 = pygame.font.Font('freesansbold.ttf', 9)
font20 = pygame.font.Font('freesansbold.ttf', 20)
font30 = pygame.font.Font('freesansbold.ttf', 30)

# --- Functions -----------------------------------------------------------------------------------



# --- Classes -------------------------------------------------------------------------------------

class colorList:

	black =		(0, 0, 0)
	white =		(255, 255, 255)
	red =		(255, 0, 0)
	cyan =		(0, 255, 255)
	green =		(0, 255, 0)
	grey =		(150, 150, 150)
	darkGrey =	(50, 50, 50)
	almostBlack =	(20, 20, 20)
	orange =	(220, 162, 57)
	green =		(70, 180, 50)
	blue =		(80, 120, 250)
	background =	(55, 55, 55)
	yellow = 	(255, 255, 0)



class the7thGame():
	""" get data from API and display it """

	def __init__(self):
		self.width = 700
		self.height = 700
		self.boardContent = [[0 for x in range(7)] for y in range(7)]
		self.boardContent[0][0] = 1
		self.boardContent[0][6] = 2
		self.boardContent[6][0] = 2
		self.boardContent[6][6] = 1
		#init gfx
		pygame.init()
		pygame.display.set_caption('The7thGame')
		self.display = pygame.display.set_mode((self.width, self.height))
		# init sounds
		self.snd_no = pygame.mixer.Sound("/home/klf/the7thGame/snd/no.mp3")
		self.snd_fail = pygame.mixer.Sound("/home/klf/the7thGame/snd/fail.mp3")
		self.playerActive = 1	# value = 0, 1 or 2
		self.running = True
		self.loop()



	def drawBackground(self):
		bckGrnd = pygame.image.load('gfx/background.png')
		self.display.blit(bckGrnd, (0, 0))



	def drawGrid(self):
		for c in [1, 100, 200, 300, 400, 500, 600, 699]:
			pygame.draw.line(self.display, colors.white, (c, 0), (c, 700), 3)
			pygame.draw.line(self.display, colors.white, (0, c), (700, c), 3)



	def drawBoard(self):
		for x in range(7):
			for y in range(7):
				xCord = x * 100 + 50
				yCord = y * 100 + 50
#				print(xCord, yCord)
				if self.boardContent[x][y] != 0:
					color = colors.blue if self.boardContent[x][y] == 1 else colors.green
					pygame.draw.circle(self.display, color, (xCord, yCord), 40)



	def _posToSquare(self, pos):
		""" Maps a mouse coordinate to one of the squares on the board or FALSE """
		posX, posY = pos
		return (posX // 100, posY // 100)



	def _pieceOnSquare(self, pos):
		""" Returns the piece on the given square; Player1, Player2 or NONE """
		posX, posY = pos
		return self.boardContent[posX][posY]


	def movePiece(self, square):
		""" Initiates movement of the chosen piece """
		sqX, sqY = square


		# 1. Calculate possible moves and show these
		# 2. check for mouseclick on ANY POSSIBLE field, and activate move if positive, else nothing (fail sound?)



		print('Moving piece on ', square)





	def checkKey(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.running = False
			elif event.type == pygame.KEYUP:
				if event.key == pygame.K_ESCAPE:
					self.running = False
				if event.key == pygame.K_q:
					self.running = False
			elif event.type == pygame.MOUSEBUTTONUP:
				pos = pygame.mouse.get_pos()
				square = self._posToSquare(pos)
				selectedPiece = self._pieceOnSquare(square)
				if selectedPiece == self.playerActive:
					self.movePiece(square)
				else:
					if selectedPiece:
						self.snd_no.play()
					else:
						self.snd_fail.play()


	def loop(self):
		""" Ensure that view runs until terminated by user """
		while self.running:
			self.drawBackground()
			self.drawGrid()
			self.drawBoard()
			pygame.display.update()
			self.checkKey()
		pygame.quit()
		print('\n  Game terminated gracefully\n')


# --- Main  ---------------------------------------------------------------------------------------

colors = colorList
obj = the7thGame()


# --- TODO ---------------------------------------------------------------------------------------
# - 



# --- NOTES --------------------------------------------------------------------------------------






