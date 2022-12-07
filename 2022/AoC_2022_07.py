def getFileContent(path):
	with open(path, "r") as file:
		return file.read()

# path = "resources/example_07.txt"
path = "resources/input_07.txt"

lines = [ s for s in getFileContent(path).split("\n") if s != "" ]

def buildFileSystem(lines):
	fileSystem = {}
	currentPath = "/" # will only contain absolute paths ended by a "/", without consecutive "/".
	for line in lines:
		splitted = line.split(" ")
		if splitted[0] == "$":
			print("Command:", splitted[1:])
			if splitted[1] == "cd":
				# N.B: input paths can be absolute or relative (starting with "." or ".."),
				# be of arbitrary depth and may or may not have an ending "/". They can also
				# contain consecutive "/" or be empty. Spaces in paths are unsupported.
				pathDirs = splitted[2].split("/") if len(splitted) > 2 else []
				currentPathDirs = currentPath.split("/")[:-1]
				for i in range(len(pathDirs)):
					if pathDirs[i] == "":
						if i == 0: # input path is absolute. Ignoring other "".
							currentPathDirs = [""]
					elif pathDirs[i] == ".": # to not add "/./" in the 'else' case.
						pass
					elif pathDirs[i] == "..":
						if len(currentPathDirs) > 1: # not in "/", moving backward.
							currentPathDirs = currentPathDirs[:-1]
					else:
						currentPathDirs += [pathDirs[i]]
				currentPath = "/".join(currentPathDirs) + "/"
				print("Current path: '%s'" % currentPath)
			elif splitted[1] == "ls":
				pass
			else:
				print("Unsupported command '%s'" % splitted[1])
				exit()
		elif splitted[0] == "dir":
			pass
		else:
			# Careful, files may not have any extension and may be visited several times.
			# Also, a same filename can exist at different places!
			filename, size = splitted[1], int(splitted[0])
			path = currentPath + filename
			pathSplitted = path.split("/")
			print("File '%s' of size %d" % (path, size))
			if path not in fileSystem:
				for i in range(1, len(pathSplitted)):
					directory = "/".join(pathSplitted[:i]) + "/"
					if directory not in fileSystem:
						fileSystem[directory] = 0
					fileSystem[directory] += size
				fileSystem[path] = size
	return fileSystem

fileSystem = buildFileSystem(lines)
print("\nFile system:", *fileSystem.items(), sep="\n")

isDirectory = lambda path : path[-1] == "/" # only works on "/" terminated paths.

directories = sorted([ c for c in fileSystem.items() if isDirectory(c[0]) ], key=lambda c : c[1])
print("\nDirectories:", *directories, sep="\n")

result = sum([ c[1] for c in directories if c[1] <= 100000 ])
print("\nResult:", result, "\n") # 2104783

# # ------------------------------------------
# # Part 2:

usedMemory, neededMemory = fileSystem["/"], 40000000
print("Used memory:", usedMemory)

toDelete = [ c for c in directories if usedMemory - c[1] <= neededMemory ][0]
print("To delete:", toDelete)
print("\nResult 2:", toDelete[1]) # 5883165
