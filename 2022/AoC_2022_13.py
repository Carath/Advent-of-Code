def getFileContent(path):
	with open(path, "r") as file:
		return file.read()

# path = "resources/example_13.txt"
path = "resources/input_13.txt"

content = [ line.split("\n") for line in getFileContent(path).split("\n\n") if line != "" ]
content = [ [ s for s in l if s != "" ] for l in content ]
content = [ [eval(c[0]), eval(c[1])] for c in content ] # evil eval
print("", *content, "", sep="\n")

def comparison(a, b):
	if type(a) == type(b) == int:
		if a < b:
			return -1
		elif a == b:
			return 0
		return 1
	elif type(a) == int and type(b) == list:
		return comparison([a], b)
	elif type(a) == list and type(b) == int:
		return comparison(a, [b])
	elif a == b:
		return 0
	elif a == []:
		return -1
	elif b == []:
		return 1
	comp = comparison(a[0], b[0])
	if comp == 0:
		return comparison(a[1:], b[1:])
	return comp

compared = [ (i, comparison(line[0], line[1])) for i, line in enumerate(content) ]

result = sum([ 1+c[0] for c in compared if c[1] < 0 ])
print("\nResult:", result, "\n") # 5330

# # ------------------------------------------
# # Part 2:

from functools import cmp_to_key

firstDivider, secondDivider = ([[2]], [[6]])

packets = [firstDivider, secondDivider]
for line in content:
	packets.append(line[0])
	packets.append(line[1])

packets.sort(key=cmp_to_key(comparison))
# print("packets:", *packets, sep="\n")

i = packets.index(firstDivider)
j = packets.index(secondDivider)

result = (i+1)*(j+1)
print("\nResult 2:", result) # 27648
