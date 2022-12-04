def getFileContent(path):
	with open(path, "r") as file:
		return file.read()

# path = "resources/example_04.txt"
path = "resources/input_04.txt"

lines = [ s for s in getFileContent(path).split("\n") if s != "" ]

pairs = [ [ [ int(z) for z in y.split("-") ] for y in x.split(",") ] for x in lines ]
print(pairs)

isIncluded = lambda p1, p2 : p2[0] <= p1[0] and p1[1] <= p2[1]

result = sum([ 1 for p in pairs if isIncluded(p[0], p[1]) or isIncluded(p[1], p[0]) ])
print("\nResult:", result, "\n") # 602

# # ------------------------------------------
# # Part 2:

doOverlap = lambda p1, p2 : max(p1[0], p2[0]) <= min(p1[1], p2[1])

result = sum([ 1 for p in pairs if doOverlap(p[0], p[1]) ])
print("\nResult 2:", result) # 891
