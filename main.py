import problem

newProblem = problem.Problem()
solve = problem.Solve_Problem()
newProblem.setStartState([[5,4,2],[7,8,3],[1,6,0]])
newProblem.setGoalState([[1,2,3],[8,0,4],[7,6,5]])

print("Goal State:")
solve.printGoalState(newProblem)
print('\n')
print("Start State:")
solve.printStartState(newProblem)
print('\n')
print("Answer:")
solve.printAnswer(newProblem)
solve.doAction(newProblem)
