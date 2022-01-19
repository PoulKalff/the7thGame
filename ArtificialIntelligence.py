import copy


class AI:
	""" calculates moves for the opponent """

	def __init__(self, game):
		self.game = game
		self.collectivePossibleMoves = []



	def _getNearSquares(self, sqX, sqY):
		""" returns two lists of surrounding squares, one of adjecent squares, the other of squares adjacent to those  """
		out = [[],[]]
		nonAdjacentSquares = []
		nonAdjacentIndexes = [24, 23, 22, 21, 20, 19, 15, 14, 11, 10, 6, 5, 4, 3, 2, 1]
		allNearSquares = 	[
								(sqX - 2, sqY - 2), (sqX - 1, sqY - 2), (sqX, sqY - 2), (sqX + 1, sqY - 2), (sqX + 2, sqY - 2), 
								(sqX - 2, sqY - 1), (sqX - 1, sqY - 1), (sqX, sqY - 1), (sqX + 1, sqY - 1), (sqX + 2, sqY - 1), 
								(sqX - 2, sqY),     (sqX - 1, sqY), 					(sqX + 1, sqY), 	(sqX + 2, sqY), 
								(sqX - 2, sqY + 1), (sqX - 1, sqY + 1), (sqX, sqY + 1), (sqX + 1, sqY + 1), (sqX + 2, sqY + 1), 
								(sqX - 2, sqY + 2), (sqX - 1, sqY + 2), (sqX, sqY + 2), (sqX + 1, sqY + 2), (sqX + 2, sqY + 2)
							]
		for x in nonAdjacentIndexes:
			nonAdjacentSquares.append(allNearSquares.pop(x - 1))
		for coord in allNearSquares:
			if -1 < coord[0] < 7 and -1 < coord[1] < 7:
				out[0].append(coord)
		for coord in nonAdjacentSquares:
			if -1 < coord[0] < 7 and -1 < coord[1] < 7:
				out[1].append(coord)
		return out



	def getPossibleMoves(self):
		""" return a list of possible moves for ALL pieces """
		self.collectivePossibleMoves = []
		for x in range(7):
			for y in range(7):
				if self.game.boardContent[x][y] == self.game.playerActive:
					self.collectivePossibleMoves += self.game._calculatePossibleMoves((x,y))
		return self.collectivePossibleMoves



	def analyzeAllMoves(self):
		""" calculates a score for all moves """
		for count in range(len(self.collectivePossibleMoves)):
			self.collectivePossibleMoves[count].score = self.analyzeMove(self.collectivePossibleMoves[count])
		# sort
		self.collectivePossibleMoves.sort(reverse=True, key=lambda x: x.score)
		# remove all moves that does not have top score, for better overview
		# --- DEV---------------------------
		if self.collectivePossibleMoves:
			temp = []
			maxValue = max(self.collectivePossibleMoves, key=lambda value: value.score).score
			for move in self.collectivePossibleMoves:
				if move.score == float(maxValue):
					temp.append(move)
			self.collectivePossibleMoves = temp
		# --- DEV---------------------------
		return True



	def analyzeMove(self, move):
		""" calculates a score for a move """
		score = 0.0
		adjacentTo, nearTo = self._getNearSquares(move.xTo, move.yTo)		# getting squares surrounding the TO-field 
		opponent = 1 if self.game.playerActive == 2 else 2
		for sqX2, sqY2 in adjacentTo:
			if self.game.boardContent[sqX2][sqY2] == opponent:
				score += 1.0
				move.scoreLog += 'C'
		if move.type == 1:
			# move is a split
			score += 1.0						# because it takes a new square
			move.scoreLog += 'Split'
		else:
			# move is a jump... check if enemy is close to square left




				# remove any captured pieces before calculating score.... how?
					# fields in "nearTo"-variable must be simulated to == playerActive!

			# clone the board to use for simulated environment
			boardClone = copy.deepcopy(self.game.boardContent)

#			print(move.show())
			for coord in adjacentTo + nearTo:
				if boardClone[coord[0]][coord[1]] == opponent:
					boardClone[coord[0]][coord[1]] = self.game.playerActive
#				print('----------', coord, boardClone[coord[0]][coord[1]])


	#		import sys
	#		sys.exit('killed for DEV')




			adjacentFrom, nearFrom = self._getNearSquares(move.xFrom, move.yFrom)		# getting squares surrounding the FROM-field 
			enemyAdjacent = False
			enemyNear = False
			opponent = 1 if self.game.playerActive == 2 else 2
			for m in adjacentFrom:
				if boardClone[m[0]][m[1]] == opponent:
					enemyAdjacent = True
			if not enemyAdjacent:
				for m in nearFrom:
					if boardClone[m[0]][m[1]] == opponent:
						enemyNear = True
			if enemyAdjacent:
				score -= 1.5
				move.scoreLog += '-Adjacent'
			elif enemyNear:
				score -= 1.0
				move.scoreLog += '-Near'
		return score




# --- NOTES --------------------------------------------------------------------------------------
#		
#		Traek de felter fra regnestykket som evt bliver overtaget ved JUMP
#		
#		
#		
#		
#		
#		


