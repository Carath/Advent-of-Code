def getFileContent(path):
	with open(path, "r") as file:
		return file.read()

# path = "resources/example_09_1.txt"
# path = "resources/example_09_2.txt"
path = "resources/input_09.txt"

moves = [ line.split(" ") for line in getFileContent(path).split("\n") if line != "" ]
# print("moves:", moves)

sign = lambda x : x // abs(x) if x != 0 else 0

def moveRope(knotsNumber):
	knots = [ [0, 0] for i in range(knotsNumber) ] # coord system: (row, col) i.e (y, x)
	visited = set([tuple(knots[0])])
	for move in moves:
		direc, steps = move[0], int(move[1])
		for s in range(steps):
			if direc == "L":
				knots[0][1] -= 1
			elif direc == "R":
				knots[0][1] += 1
			elif direc == "U":
				knots[0][0] -= 1
			elif direc == "D":
				knots[0][0] += 1
			else:
				print("Unsupported direction '%s'" % direc)
			for i in range(1, knotsNumber):
				deltaRow, deltaCol = knots[i-1][0]-knots[i][0], knots[i-1][1]-knots[i][1]
				dist = max(abs(deltaRow), abs(deltaCol))
				if dist > 1:
					knots[i][0] += sign(deltaRow)
					knots[i][1] += sign(deltaCol)
			visited.add(tuple(knots[knotsNumber-1]))
	return visited

visited = moveRope(2)
# print("visited:", visited)

result = len(visited)
print("\nResult:", result, "\n") # 6357

# # ------------------------------------------
# # Part 2:

visited = moveRope(10)
# print("visited:", visited)

result = len(visited)
print("\nResult 2:", result) # 2627
