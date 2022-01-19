
class Move:
	""" A move on the board """

	def __init__(self, fx, fy, tx, ty):
		self.xFrom = fx
		self.yFrom = fy
		self.xTo = tx
		self.yTo = ty
		self.score = None
		self.scoreLog = ''
		self.type = 2 if abs(self.xFrom - self.xTo) > 1 or abs(self.yFrom - self.yTo) > 1 else 1


	def show(self):
		return '(' + str(self.xFrom) + ',' + str(self.yFrom) + ' ---> ' + str(self.xTo) + ',' + str(self.yTo) + ') : SCORE=' + str(self.score) + ' TYPE=' + str(self.type) + ' LOG=' + self.scoreLog



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
					movesTo = self.game._calculatePossibleMoves((x,y))
					for xTo, yTo in movesTo:
						self.collectivePossibleMoves.append(Move(x, y, xTo, yTo))
		return self.collectivePossibleMoves



	def analyzeAllMoves(self):
		""" calculates a score for all moves """
		for count in range(len(self.collectivePossibleMoves)):
			self.collectivePossibleMoves[count].score = self.analyzeMove(self.collectivePossibleMoves[count])
		# sort
		self.collectivePossibleMoves.sort(reverse=True, key=lambda x: x.score)
		# (for DEV): remove all moves that does not have top score, for better overview
		if self.collectivePossibleMoves:
			temp = []
			maxValue = max(self.collectivePossibleMoves, key=lambda value: value.score).score
			for move in self.collectivePossibleMoves:
				if move.score == maxValue:
					temp.append(move)
			self.collectivePossibleMoves = temp
		# (for DEV): remove all moves that does not have top score, for better overview
		return True



	def analyzeMove(self, move):
		""" calculates a score for a move """
		score = 0
		adjacentTo, nearTo = self._getNearSquares(move.xTo, move.yTo)		# getting squares surrounding the TO-field 
		opponent = 1 if self.game.playerActive == 2 else 2
		for sqX2, sqY2 in adjacentTo:
			if self.game.boardContent[sqX2][sqY2] == opponent:
				score += 1
				move.scoreLog += 'C'


		print(move.show())



		if move.type == 1:
			# move is a split
			score += 1						# because it takes a new square
			move.scoreLog += 'Split'
		else:
			# move is a jump
			score += 0
			adjacentFrom, nearFrom = self._getNearSquares(move.xFrom, move.yFrom)		# getting squares surrounding the FROM-field 




			# calulate negtive points for leaving square open
			#	-1 for each own piece left, but ONLY if opponent has piece within 2 squares to take it
			#	PREFER to take where there are no neighbors

		return score








# --- NOTES --------------------------------------------------------------------------------------
#		
#		
#		
#		
#		
#		
#		
#		


