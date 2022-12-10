def getFileContent(path):
	with open(path, "r") as file:
		return file.read()

# path = "resources/example_10.txt"
path = "resources/input_10.txt"

lines = [ line.split(" ") for line in getFileContent(path).split("\n") if line != "" ]
# print(lines)

width, height = 40, 6
screen = [ ['.'] * width for i in range(height) ]
cycles, X, samples = 0, 1, []

def processCycle():
	global cycles
	cycles += 1
	if (cycles - width//2) % width == 0:
		samples.append(cycles * X)
	pixelRow = ((cycles - 1) // width) % height
	pixelCol = (cycles - 1) % width
	if abs(pixelCol-X) <= 1:
		screen[pixelRow][pixelCol] = '#'

for line in lines:
	if line[0] == "noop":
		processCycle()
	else: # addx
		processCycle()
		processCycle()
		X += int(line[1])

print("Total cycles:", cycles)
print("samples:", samples)

result = sum(samples)
print("\nResult:", result, "\n") # 15680

# # ------------------------------------------
# # Part 2:

print("screen:", *[ "".join(row) for row in screen ], sep="\n")

# Read result from the console. Here: ZFBFHGUP
