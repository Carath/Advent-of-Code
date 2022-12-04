def getFileContent(path):
	with open(path, "r") as file:
		return file.read()

# path = "resources/example_02.txt"
path = "resources/input_02.txt"

content = getFileContent(path)
content = [ x.split(" ") for x in content.split("\n") if x != "" ]
# print(content)

states = ["A", "B", "C"]

convertLetter = lambda x : chr(ord(x) - 23)

def score(choice):
	opponent, our = choice
	i, j = states.index(opponent), states.index(convertLetter(our))
	if (i+1) % 3 == j: # win
		return j + 7
	elif i == j: # draw
		return j + 4
	else: # lose
		return j + 1

result = sum([ score(x) for x in content ])
print("\nResult:", result) # 13526

# # ------------------------------------------
# # Part 2:

def score_2(choice):
	opponent, our = choice
	i, j = states.index(opponent), states.index(convertLetter(our))
	return 3 * j + (i+j-1) % 3 + 1

result = sum([ score_2(x) for x in content ])
print("\nResult 2:", result) # 14204
