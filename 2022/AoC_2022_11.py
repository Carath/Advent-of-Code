import copy

def getFileContent(path):
	with open(path, "r") as file:
		return file.read()

# path = "resources/example_11.txt"
path = "resources/input_11.txt"

data = getFileContent(path).replace(",", "").split("\n\n")
data = [ s.split("\n") for s in data if s != "" ]
data = [ [ s.split() for s in l ] for l in data ]
data = { int(l[0][-1][:-1]): [ [ int(s) for s in l[1][2:] ], l[2][3:],
	int(l[3][-1]), int(l[4][-1]), int(l[5][-1]), 0] for l in data } # last value: added total item count

print("data:", *data.items(), "", sep="\n")

getVal = lambda item, val : item if val == "old" else int(val)

gcd = lambda a, b : a if b == 0 else gcd(b, a % b)
lcm = lambda a, b : a * b // gcd(a, b)
lcm_list = lambda l : 1 if l == [] else lcm(l[0], lcm_list(l[1:]))

integerBound = lcm_list([ d[-4] for d in data.values() ])
print("Integer bound:", integerBound, "\n") # no need to go further when no relief.

def goMonkeys(data, rounds, relief):
	data = copy.deepcopy(data)
	monkeysNumber = max(data.keys())+1
	for i in range(rounds):
		for monkey in range(monkeysNumber):
			for item in data[monkey][0]:
				worry, op, val = item, data[monkey][1][-2], data[monkey][1][-1]
				if op == "*":
					worry *= getVal(item, val)
				elif op == "+":
					worry += getVal(item, val)
				elif op == "-":
					worry -= getVal(item, val)
				elif op == "/":
					worry //= getVal(item, val)
				else:
					print("Unsupported operation '%s'" % op)
					exit()
				worry = worry // 3 if relief else worry % integerBound
				idx = -3 if worry % data[monkey][-4] == 0 else -2
				nextMonkey = data[monkey][idx]
				data[nextMonkey][0].append(worry)
			data[monkey][-1] += len(data[monkey][0])
			data[monkey][0] = []
		# print("End of round %d\ndata:" % (i+1), *data.items(), "", sep="\n")
	return data

newData = goMonkeys(data, 20, True)
print("newData:", *newData.items(), "", sep="\n")

activities = sorted([ d[-1] for d in newData.values() ], reverse=True)
print("activities:", activities)

result = activities[0] * activities[1]
print("\nResult:", result, "\n") # 102399

# # ------------------------------------------
# # Part 2:

newData = goMonkeys(data, 10000, False)
print("newData:", *newData.items(), "", sep="\n")

activities = sorted([ d[-1] for d in newData.values() ], reverse=True)
print("activities:", activities)

result = activities[0] * activities[1]
print("\nResult 2:", result) # 23641658401 in 0.43 s
