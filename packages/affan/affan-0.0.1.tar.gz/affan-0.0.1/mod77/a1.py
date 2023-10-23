'''


from collections import defaultdict

jug1, jug2, aim = 4, 3, 2

visited = defaultdict(lambda: False)


def waterJugSolver(amt1, amt2):

	if (amt1 == aim and amt2 == 0) or (amt2 == aim and amt1 == 0):
		print(amt1, amt2)
		return True
	
	if visited[(amt1, amt2)] == False:
		print(amt1, amt2)
	
		visited[(amt1, amt2)] = True
	
		return (waterJugSolver(0, amt2) or
				waterJugSolver(amt1, 0) or
				waterJugSolver(jug1, amt2) or
				waterJugSolver(amt1, jug2) or
				waterJugSolver(amt1 + min(amt2, (jug1-amt1)),
				amt2 - min(amt2, (jug1-amt1))) or
				waterJugSolver(amt1 - min(amt1, (jug2-amt2)),
				amt2 + min(amt1, (jug2-amt2))))
	
	else:
		return False

print("Steps: ")

waterJugSolver(0, 0)


---------------------------------------------------------------------------------


import random

# Define a function to evaluate the current solution
def evaluate_solution(solution):
    # Example: Minimize a simple function (you can replace this with your own problem)
    return sum(x ** 2 for x in solution)

# Hill Climbing Algorithm
def hill_climbing(problem_size, iterations):
    current_solution = [random.uniform(-5, 5) for _ in range(problem_size)]
    current_value = evaluate_solution(current_solution)

    for _ in range(iterations):
        neighbor_solution = [x + random.uniform(-0.1, 0.1) for x in current_solution]
        neighbor_value = evaluate_solution(neighbor_solution)

        if neighbor_value < current_value:
            current_solution = neighbor_solution
            current_value = neighbor_value

    return current_solution, current_value

# Example usage
problem_size = 5  # Change this to the size of your problem
iterations = 100  # Number of iterations

best_solution, best_value = hill_climbing(problem_size, iterations)

print("Best Solution:", best_solution)
print("Best Value:", best_value)







-----------------------------------------------------------------------------------------------------


 '''

def sum(n1,n2):
    c=n1+n2