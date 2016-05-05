import heapq
import copy

class Problem:

	def __init__(self):
		"""
		"""
		self.nodeExpanded = 0
		self.startState = []
		self.nonePosition = None
		self.dicGoal = dict()

	def findNonePosition(self, matrix):
		""" find position of "0" in matrix """

		for i in range(len(matrix)):
			for j in range(len(matrix[0])):
				if matrix[i][j] == 0:
					return (i, j)

	"""
	def setStartState(self):
		startState = []
		for i in range(3):
			temp = []
			for j in range(3):
				num = int(input())
				if num == 0:
					self.nonePosition = (i, j)
				temp.append(num)
			startState.append(temp)


		self.startState = startState
	"""

	def setStartState(self, matrix):

		self.startState = matrix[:]

		# find position of "0"
		self.nonePosition = self.findNonePosition(self.startState)

	def getStartState(self):
		""" 
		return Start State
		state stored in array
		-> ([], localNone)
		"""
		"""
		self.startSate =[[5,4,2],[7,8,3],[1,6,0]]
		nonePosition = (2,2)
		"""

		return (self.startState, self.nonePosition)

	def setGoalState(self, matrix):
		""" Set goal state equal to matrix """
		self.goalState = matrix[:]

		# create dicGoal to calculate heuristic value
		for i in range(len(matrix)):
			for j in range(len(matrix[0])):
				self.dicGoal[matrix[i][j]] = (i, j)

		

	def getGoalState(self):
		"""
		return Goal State 
		state stored in array with '0' is None-node
		"""
		"""
		goalState = [[1,2,3],[8,0,4],[7,6,5]]
		nonePosition = (1,1)
		dicGoal = {1: (0,0), 2 : (0,1), 3 : (0, 2), 8 : (1, 0), 0 : (1, 1), 4 : (1, 2), 7 : (2, 0), 6 : (2, 1), 5 : (2, 2)}
		"""

		return (self.goalState, self.dicGoal)

	def isGoadState(self, state):
		"""
		True: if state is Goal State
		False: if not
		with state is ([], cost)
		"""
		goalState = self.getGoalState()

		return state[0] == goalState[0]

	def isValidPosition(self, nextx, nexty):
		"Check valid of newPosition"

		if nextx < 0 or nextx >= 3:
			return False
		if nexty < 0 or nexty >= 3:
			return False
		return True

	

	def getSuccessors(self, state):
		"""
		return successor of current state
		"""
		direction = Direction()
		
		successors = []
		cost = 1
		#print(state, '\n')
		x,y = state[1]
		for action in direction.listDirection:
			matrix = copy.deepcopy(state[0])
			dx, dy = action
			nextx, nexty = int(x+dx), int(y+dy)

			if self.isValidPosition(nextx, nexty):
				#print(self.isValidPosition(nextx, nexty))
				#swap position
				temp = matrix[x][y]
				matrix[x][y] = matrix[nextx][nexty]
				matrix[nextx][nexty] = temp
				nextState = (matrix, (nextx, nexty))
				successors.append((nextState, direction.toString(action), cost, nextState[1]))
		
		#print("successors: ", successors)

		self.nodeExpanded += 1
		return successors


class PriorityQueue:
	"""

	"""
	def __init__(self):
		self.heap = []
		self.count = 0

	def push(self, item, priority):
		# restored old behavior to check against old results better
		# restored to stable behaviour

		entry = (priority, self.count, item)
		heapq.heappush(self.heap, entry)
		self.count += 1
	def pop(self):
		(_, _, item) = heapq.heappop(self.heap)

		return item

	def isEmpty(self):
		return len(self.heap) == 0



class Direction:
	"With 4 direction "
	def __init__(self):
		n = 3 # 'n' is height of matrix
		self.NORTH = (-1, 0)
		self.SOUTH = (1, 0)
		self.EAST = (0, 1)
		self.WEST = (0, -1)
		self.listDirection = [self.NORTH, self.SOUTH, self.EAST, self.WEST]
		self.dicDirection = {self.NORTH : 'North', self.SOUTH : 'South', self.EAST : 'East', self.WEST : 'West'}
		self.tempDictionary = {'North' : self.NORTH, 'South' : self.SOUTH, 'East' : self.EAST, 'West' : self.WEST}

	def toString(self, direction):
		return self.dicDirection[direction]



class Solve_Problem:
	def __init__(self):
		"""
		"""

	def aStarSearch(self, problem):
		"""
		A heuristic function estimates the cost from the current state to 
		the nearest goal in the provided. 
		"""

		frontier = PriorityQueue()
		startState = problem.getStartState()
		curState = [startState, [], 0.0, [startState[1]]]
		visited_state = []

		while not problem.isGoadState(curState[0]):
			curNode, cur_dir, cur_cost, nonePositionMove = curState
			if curNode not in visited_state:
				visited_state.append(curNode)
				for nextState, direction, cost, nonePosition in problem.getSuccessors(curNode):
					frontier.push((nextState, cur_dir + [direction], cur_cost + cost, nonePositionMove + [nonePosition]), cur_cost + cost + self.heuristicFunction(nextState, problem))
				
			curState = frontier.pop()
		return curState

	def getAnswer(self, problem):
		""" Get answer for problem
		return: a tupe contain (nonePositionMove, cost, nodeExpanded)
				nonePositionMove: list changing of "0" position
				nodeExpanded: total node expanded 
		"""
		goalState, moveDirection, cost, nonePositionMove = self.aStarSearch(problem)

		return (nonePositionMove, problem.nodeExpanded)

	def printState(self, state):
		
		 matrix = state
		 for x in matrix:
		 	for y in x:
		 		print(y, end=" ")
		 	print('\n')
	def printGoalState(self, problem):
		goalState = problem.getGoalState()
		self.printState(goalState[0])

	def printStartState(self, problem):
		startSate = problem.getStartState()
		self.printState(startSate[0])

	def printAnswer(self, problem):
		answer = self.aStarSearch(problem)
		state, direction, cost, nonePositionMove = answer
		
		self.printState(state[0])
		print(direction)
		print("Node Expanded: ", problem.nodeExpanded)
		print("Cost: ", cost)
		


	def heuristicFunction(self, state, problem):
		"return heuristic value"
		heuristicValue = 0
		wrongPosition = 0
		distance = 0
		matrix, nonePosition = state

		goalState = problem.getGoalState()
		goalMatrix, dicGoal = goalState
		length = len(matrix[0])
		for x in range(0, length):
			for y in range(0, length):
				if matrix[x][y] != goalMatrix[x][y]:
					wrongPosition += 1
					dx, dy = dicGoal[matrix[x][y]]
					distance += (abs(x - dx) + abs(y - dy))
		heuristicValue = distance + wrongPosition
		
		return heuristicValue


	def doAction(self, problem):
		direction = Direction()
		startSate = problem.getStartState()
		answer = self.aStarSearch(problem)
		matrix, nonePosition = startSate
		x, y = nonePosition
		print("Answer: ", answer)
		for item in answer[1]:
			dx, dy = direction.tempDictionary[item]
			nextx, nexty = int(x+dx), int(y+dy)
			temp = matrix[x][y]
			matrix[x][y] = matrix[nextx][nexty]
			matrix[nextx][nexty] = temp
			x, y = nextx, nexty
			print(x,y, item,'\n')
			self.printState(matrix)
			#print(problem.isGoadState((matrix, (x,y))))
			print('\n')






