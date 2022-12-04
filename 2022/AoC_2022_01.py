def getFileContent(path):
	with open(path, "r") as file:
		return file.read()

# path = "resources/example_01.txt"
path = "resources/input_01.txt"

content = getFileContent(path)
# print(content)

calories = [ sum([ int(y) for y in x.split("\n") if y != "" ]) for x in content.split("\n\n") ]
print(calories)

result = max(calories)
print("\nResult:", result) # 68802

# ------------------------------------------
# Part 2:

calories.sort(reverse=True)

result = sum(calories[0:3])
print("\nResult 2:", result) # 205370
