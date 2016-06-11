import problem
import time

newProblem = problem.Problem()
solve = problem.Solve_Problem()

matrix = []
for i in range(3):
	temp = []
	for j in range(3):
		temp.append(int(input()))
	matrix.append(temp)

#matrix = [[2,1,3],[8,0,4],[6,7,5]]


newProblem.setStartState(matrix)
newProblem.setGoalState([[1,2,3],[8,0,4],[7,6,5]])

print("Goal State:")
solve.printGoalState(newProblem)
print('\n')
print("Start State:")
solve.printStartState(newProblem)
print('\n')
print("Answer:")
start_time = time.time()
nonPositionMove, cost, nodeExpanded = solve.getAnswer(newProblem)
print("Cost: ", cost)
print("Node Expanded: ", nodeExpanded)
print("Time: %s seconds" %(time.time() - start_time))
print("\n")
solve.doAction(newProblem)

