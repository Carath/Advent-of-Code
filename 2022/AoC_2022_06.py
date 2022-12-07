def getFileContent(path):
	with open(path, "r") as file:
		return file.read()

# path = "resources/example_06.txt"
path = "resources/input_06.txt"

content = getFileContent(path)

def findMarker(s, k):
	for i in range(len(s)-k):
		chunk = s[i:i+k]
		if len(set(list(chunk))) == k:
			print("marker:", chunk)
			return i+k

result = findMarker(content, 4)
print("\nResult:", result, "\n") # 1702

# # ------------------------------------------
# # Part 2:

result = findMarker(content, 14)
print("\nResult 2:", result) # 3559
