def getFileContent(path):
	with open(path, "r") as file:
		return file.read()

# path = "resources/example_03.txt"
path = "resources/input_03.txt"

lines = [ s for s in getFileContent(path).split("\n") if s != "" ]

rucksacks = [ (s[:len(s)//2], s[len(s)//2:]) for s in lines ]
print("rucksacks:", rucksacks, "\n")

intersections = [ set(r[0]) & set(r[1]) for r in rucksacks ]
print("intersections:", intersections, "\n")

priority = lambda c : ord(c) - (96 if ord(c) > 96 else 38)

# print([ priority(x) for x in ['a', 'z', 'A', 'Z'] ])

result = sum([ priority(list(x)[0]) for x in intersections ])
print("\nResult:", result, "\n") # 8515

# # ------------------------------------------
# # Part 2:

groups = [ lines[i:i+3] for i in range(0, len(lines), 3) ]
print("groups:", groups, "\n")

badges = [ set(g[0]) & set(g[1]) & set(g[2]) for g in groups ]
print("badges:", badges, "\n")

result = sum([ priority(list(x)[0]) for x in badges ])
print("\nResult 2:", result) # 2434
