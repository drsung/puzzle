import problem

# Example solve problem

newProblem = problem.Problem()
solve = problem.Solve_Problem()

print("Goal State:")
solve.printGoalState(newProblem)
print('\n')
print("Start State:")
solve.printStartState(newProblem)
print('\n')
print("Answer:")
solve.printAnswer(newProblem)
solve.doAction(newProblem)
