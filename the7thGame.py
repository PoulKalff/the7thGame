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


# --- Variables / Ressources ----------------------------------------------------------------------

pygame.init()
version = '0.5'	# added jump-logic
playerColors = { 1 : (80, 120, 250), 2 : (70, 180, 50) }
sounds =	{
					'no' :		pygame.mixer.Sound("snd/no.mp3"),
					'fail' :	pygame.mixer.Sound("snd/fail.mp3"),
					'noMoves' : pygame.mixer.Sound("snd/nomoves.mp3")
			}
background = pygame.image.load('gfx/background.png')
font30 = pygame.font.Font('freesansbold.ttf', 30)
font60 = pygame.font.Font('freesansbold.ttf', 60)


# --- Functions -----------------------------------------------------------------------------------

def dumpSquares(squares):
	""" Helper function to visualize squares """
	return 'notImplemented Error'


# --- Classes -------------------------------------------------------------------------------------

class colorList:

	black =			(0, 0, 0)
	white =			(255, 255, 255)
	red =			(255, 0, 0)
	cyan =			(0, 255, 255)
	green =			(0, 255, 0)
	grey =			(150, 150, 150)
	lightGrey =		(150, 150, 150)
	almostBlack =	(20, 20, 20)
	orange =		(220, 162, 57)
	green =			(70, 180, 50)
	blue =			(80, 120, 250)
	background =	(55, 55, 55)
	yellow = 		(255, 255, 0)



class the7thGame():
	""" get data from API and display it """

	def __init__(self):
		self.width = 700
		self.height = 750
		self.resetGame()
		pygame.init()
		pygame.display.set_caption('The7thGame')
		self.display = pygame.display.set_mode((self.width, self.height))
		self.running = True
		self.loop()



	def drawBoard(self):
		# draw background
		self.display.blit(background, (0, 0))
		# draw grid
		for c in [1, 100, 200, 300, 400, 500, 600, 699]:
			pygame.draw.line(self.display, colors.white, (c, 0), (c, 700), 3)
			pygame.draw.line(self.display, colors.white, (0, c), (700, c), 3)
		# draw all pieces on the board, draw all possible moves
		self.score = [0, 0]
		for x in range(7):
			for y in range(7):
				xCord = x * 100 + 50
				yCord = y * 100 + 50
				if self.boardContent[x][y] != 0:
					if self.boardContent[x][y] == 1:
						color = colors.blue
						self.score[0] += 1
					else:
						color = colors.green
						self.score[1] += 1
					pygame.draw.circle(self.display, colors.lightGrey , (xCord, yCord), 40)
					pygame.draw.circle(self.display, color, (xCord, yCord), 37)
		# draw possible moves, if any
		for x, y  in self.possibleMoves:
			coordX = x * 100 + 50
			coordY = y * 100 + 50
			pygame.draw.circle(self.display, colors.red, (coordX, coordY), 10)
		# draw status area
		scoreA = str(self.score[0]) if self.score[0] > 9 else '0' + str(self.score[0])
		scoreB = str(self.score[1]) if self.score[1] > 9 else '0' + str(self.score[1])
		text1 = font30.render('Player to move : ', True, colors.white)
		if not self.winner:
			text2 = font30.render('Player ' + str(self.playerActive), True, playerColors[self.playerActive] )
		else:
			text2 = font30.render('None', True, colors.red )
		text3 = font30.render('Score : ', True, colors.white )
		text4 = font30.render(scoreA, True, colors.blue )
		text5 = font30.render('/', True, colors.white )
		text6 = font30.render(scoreB, True, colors.green )
		pygame.draw.rect(self.display, colors.black, (0, 700, 700, 50))	
		self.display.blit(text1, (10, 710))
		self.display.blit(text2, (260, 710))
		self.display.blit(text3, (420, 710))
		self.display.blit(text4, (550, 710))
		self.display.blit(text5, (605, 710))
		self.display.blit(text6, (630, 710))
		pygame.draw.line(self.display, colors.white, (1, 700), (1, 750), 3)
		pygame.draw.line(self.display, colors.white, (699, 700), (699, 750), 3)
		pygame.draw.line(self.display, colors.white, (0, 750), (700, 750), 3)
		pygame.draw.line(self.display, colors.white, (400, 705), (400, 742), 3)




	def _posToSquare(self, pos):
		""" Maps a mouse coordinate to one of the squares on the board or FALSE """
		posX, posY = pos
		return (posX // 100, posY // 100)



	def _pieceOnSquare(self, pos):
		""" Returns the piece on the given square; Player1, Player2 or NONE """
		posX, posY = pos
		return self.boardContent[posX][posY]



	def _calculatePossibleMoves(self, square):
		""" Returns the possible moves from a given position """
		sqX, sqY = square
		possibleMoves = []
		allMoves =	[
						(sqX - 2, sqY - 2), (sqX - 1, sqY - 2), (sqX, sqY - 2), (sqX + 1, sqY - 2), (sqX + 2, sqY - 2), 
						(sqX - 2, sqY - 1), (sqX - 1, sqY - 1), (sqX, sqY - 1), (sqX + 1, sqY - 1), (sqX + 2, sqY - 1), 
						(sqX - 2, sqY),     (sqX - 1, sqY), 					(sqX + 1, sqY), 	(sqX + 2, sqY), 
						(sqX - 2, sqY + 1), (sqX - 1, sqY + 1), (sqX, sqY + 1), (sqX + 1, sqY + 1), (sqX + 2, sqY + 1), 
						(sqX - 2, sqY + 2), (sqX - 1, sqY + 2), (sqX, sqY + 2), (sqX + 1, sqY + 2), (sqX + 2, sqY + 2)
					]
		for coord in allMoves:
			if -1 < coord[0] < 7 and -1 < coord[1] < 7:
				if self.boardContent[coord[0]][coord[1]] == 0:
					possibleMoves.append(coord)
		return possibleMoves



	def executeMove(self, squareFrom, squareTo):
		""" Calculate changes resulting from move """
		sqX, sqY = squareTo
		opponent = 1 if self.playerActive == 2 else 2
		self.possibleMoves = []
		# show piece move
		self.drawBoard()
		if abs(squareFrom[0] - squareTo[0]) > 1 or abs(squareFrom[1] - squareTo[1]) > 1:	# if distance is more than 1 square
			self.jumpAnimation(squareFrom, squareTo)
		else:
			self.moveAnimation(squareFrom, squareTo)
		self.drawBoard()
		# calculate adjacent squares occupied by opponent
		adjacentSquares = []
		allAdjacentSquares =	[
									(sqX - 1, sqY - 1), (sqX, sqY - 1), (sqX + 1, sqY - 1), 
									(sqX - 1, sqY), 					(sqX + 1, sqY), 
									(sqX - 1, sqY + 1), (sqX, sqY + 1), (sqX + 1, sqY + 1)
								]
		for coord in allAdjacentSquares:
			if -1 < coord[0] < 7 and -1 < coord[1] < 7:
				if self.boardContent[coord[0]][coord[1]] != self.playerActive:
					adjacentSquares.append(coord)
		for sqX2, sqY2 in adjacentSquares:
			if self.boardContent[sqX2][sqY2] == opponent:
				self.takeoverAnimation((sqX2, sqY2))
				self.boardContent[sqX2][sqY2] = self.playerActive
		self.stage = 1
		self.movingFrom = None
		self.playerActive = 1 if self.playerActive == 2 else 2
		return True



	def checkStatus(self):
		""" Check if any player has no pieces left, and end game if true """
		# does active player have possible moves?
		collectivePossibleMoves = []
		for x in range(7):
			for y in range(7):
				if self.boardContent[x][y] == self.playerActive:
					collectivePossibleMoves += self._calculatePossibleMoves((x,y))
		if not collectivePossibleMoves:
			self.winner = self.playerActive
			condition = "Player can't  move"
		# are all squares taken?
		if self.score[0] + self.score[1] == 49:
			self.winner = 1 if self.score[0] > self.score[1] else 2
			condition = 'Winner  on  score'
		# is a player eliminiated?
		elif self.score[0] == 0:
			self.winner = 2
			condition = 'Player eliminated'
		elif self.score[1] == 0:
			self.winner = 1
			condition = 'Player eliminated'
		if self.winner:
			text1 = font60.render('Congratulations', True, colors.red )
			text2 = font60.render('Player ' + str(self.winner), True, colors.black )
			text3 = font60.render('Player ' + str(self.winner), True, playerColors[self.winner] )
			text4 = font60.render('You Win Game!', True, colors.red )
			text5 = font30.render('(' + condition + ')', True, colors.red )
			text6 = font30.render('Press Spacebar to play again or ESC to quit', True, colors.red )
			self.display.blit(text1, (106, 120))
			self.display.blit(text2, (228, 218))
			self.display.blit(text2, (228, 222))
			self.display.blit(text2, (232, 218))
			self.display.blit(text2, (232, 222))
			self.display.blit(text3, (230, 220))
			self.display.blit(text4, (130, 320))
			self.display.blit(text5, (203, 435))
			self.display.blit(text6, (30, 535))
		return True



	def resetGame(self):
		self.boardContent = [[0 for x in range(7)] for y in range(7)]
		self.boardContent[0][0] = 1
		self.boardContent[0][6] = 2
		self.boardContent[6][0] = 2
		self.boardContent[6][6] = 1
		self.possibleMoves = []
		self.playerActive = 1	# value = 0, 1 or 2
		self.stage = 1	# either 1 = selectPiece or 2 = movePiece
		self.score = [2, 2]
		self.winner = 0



	def jumpAnimation(self, fromSquare, toSquare):
		""" Shows simple animation of a piece jumping 2 squares"""
		self.boardContent[fromSquare[0]][fromSquare[1]] = 0
		xFrom = fromSquare[0] * 100 + 50
		yFrom = fromSquare[1] * 100 + 50
		xTo =   toSquare[0]   * 100 + 50
		yTo =   toSquare[1]   * 100 + 50
		xDistance = xFrom - xTo
		yDistance = yFrom - yTo
		xCord = xFrom
		yCord = yFrom
		radius = 37
		# execute move
		for step in range(20):
			if step <= 10:
				radius += 4
			else:
				radius -= 4
			xCord -= 10 * (xDistance / 200)
			yCord -= 10 * (yDistance / 200)
			self.drawBoard()
			pygame.draw.circle(self.display, colors.lightGrey , (xCord, yCord), int(radius) + 3)
			pygame.draw.circle(self.display, playerColors[self.playerActive], (xCord, yCord), int(radius))
			pygame.display.update()
			time.sleep(0.01)
		self.boardContent[toSquare[0]][toSquare[1]] = self.playerActive
		return True



	def takeoverAnimation(self, square):
		""" Shows simple animation of a piece taken by another """
		xCord = square[0] * 100 + 50
		yCord = square[1] * 100 + 50
		for radius in range(1, 38):
			pygame.draw.circle(self.display, playerColors[self.playerActive], (xCord, yCord), radius)
			pygame.display.update()
			time.sleep(0.01)
		return True



	def moveAnimation(self, fromSquare, toSquare):
		""" Shows simple animation of a piece moved from/to square """
		self.boardContent[toSquare[0]][toSquare[1]] = self.playerActive
		xFrom = fromSquare[0] * 100 + 50
		yFrom = fromSquare[1] * 100 + 50
		xTo =   toSquare[0]   * 100 + 50
		yTo =   toSquare[1]   * 100 + 50
		xDistance = xFrom - xTo
		yDistance = yFrom - yTo
		xCord = xFrom
		yCord = yFrom
		# execute move
		for radius in range(100):
			xCord -= (xDistance / 100)
			yCord -= (yDistance / 100)
			pygame.draw.circle(self.display, playerColors[self.playerActive], (xCord, yCord), 30)
			pygame.display.update()
			time.sleep(0.001)
		return True



	def checkInput(self):
		""" Checks and responds to input from keyboard and mouse """
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.running = False
			elif event.type == pygame.KEYUP:
				if event.key == pygame.K_ESCAPE:
					self.running = False
				elif event.key == pygame.K_q:
					self.running = False
				elif event.key == pygame.K_SPACE:
					if self.winner:
						self.resetGame()
			elif not self.winner and event.type == pygame.MOUSEBUTTONUP:
				pos = pygame.mouse.get_pos()
				square = self._posToSquare(pos)
				selectedPiece = self._pieceOnSquare(square)
				if self.stage == 1:								# select piece
					if selectedPiece == self.playerActive:
						self.movingFrom = square
						self.possibleMoves =  self._calculatePossibleMoves(square)
						if self.possibleMoves:
							self.stage = 2
						else:
							sounds['noMoves'].play()
					else:
						if selectedPiece:
							sounds['no'].play()
						else:
							sounds['fail'].play()
				elif self.stage == 2:							# move piece
					# get the selected square
					if square in self.possibleMoves:
						self.executeMove(self.movingFrom, square)
					elif square == self.movingFrom:
						self.stage = 1
						self.movingFrom = None
						self.possibleMoves = []
					else:
						sounds['fail'].play()



	def loop(self):
		""" Ensure that view runs until terminated by user """
		while self.running:
			self.drawBoard()
			self.checkInput()
			self.checkStatus()
			pygame.display.update()
		pygame.quit()
		print('\n  Game terminated gracefully\n')


# --- Main  ---------------------------------------------------------------------------------------

colors = colorList
obj = the7thGame()


# --- TODO ---------------------------------------------------------------------------------------
# - include all animations in main frame
# - AI



# --- NOTES --------------------------------------------------------------------------------------






