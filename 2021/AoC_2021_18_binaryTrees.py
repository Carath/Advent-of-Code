class BinaryTree: # Those trees can be travelled up and down!

	def __init__(self, left, right=None, parent=None):
		self.left = left # leaves have content in 'left'
		self.right = right
		self.parent = parent

	def toString(self):
		if self.right == None:
			return str(self.left)
		return '[%s,%s]' % (self.left.toString(), self.right.toString())

	def print(self):
		print(self.toString())

	def copy(self, parent=None):
		if self.right == None:
			return BinaryTree(self.left, parent=parent)
		bt = BinaryTree(None, parent=parent)
		bt.left = self.left.copy(bt)
		bt.right = self.right.copy(bt)
		return bt

	# Creates a whole new tree:
	@staticmethod
	def fusion(tree_1, tree_2):
		bt = BinaryTree(tree_1.copy(), tree_2.copy())
		bt.left.parent = bt
		bt.right.parent = bt
		return bt

	@staticmethod
	def fromString(string, parent=None):
		assert string != '', 'Empty string!'
		if string[0] != '[':
			return BinaryTree(int(string), parent=parent)
		idx = getClosingIdx(string, 1) if string[1] == '[' else string.find(',')
		assert idx != -1, 'Invalid string: %s' % string
		bt = BinaryTree(None, parent=parent)
		bt.left = BinaryTree.fromString(string[1:idx], bt)
		bt.right = BinaryTree.fromString(string[idx+1:-1], bt)
		return bt

	def findClosestLeft(self, up=True):
		if up:
			parent = self.parent
			if parent == None:
				return None
			if parent.left == self: # address equality
				return parent.findClosestLeft()
			return parent.left.findClosestLeft(False)
		elif self.right == None:
			return self
		return self.right.findClosestLeft(False)

	def findClosestRight(self, up=True):
		if up:
			parent = self.parent
			if parent == None:
				return None
			if parent.right == self: # address equality
				return parent.findClosestRight()
			return parent.right.findClosestRight(False)
		elif self.right == None:
			return self
		return self.left.findClosestRight(False)

	def findExplosion(self, depth=0):
		if self.right == None:
			return None
		if depth >= 4 and self.left.right == None and self.right.right == None:
			return self
		result = self.left.findExplosion(depth+1) # trying to find the leftmost one.
		if result != None:
			return result
		return self.right.findExplosion(depth+1)

	def findSplit(self):
		if self.right == None:
			return self if self.left >= 10 else None
		result = self.left.findSplit() # trying to find the leftmost one.
		if result != None:
			return result
		return self.right.findSplit()

	def explode(self):
		toExplode = self.findExplosion()
		if toExplode == None:
			return False
		closestLeft = toExplode.findClosestLeft()
		closestRight = toExplode.findClosestRight()
		if closestLeft != None:
			closestLeft.left += toExplode.left.left
		if closestRight != None:
			closestRight.left += toExplode.right.left
		toExplode.left = 0
		toExplode.right = None
		return True

	def split(self):
		toSplit = self.findSplit()
		if toSplit == None:
			return False
		value = toSplit.left
		toSplit.left = BinaryTree(value // 2, None, toSplit)
		toSplit.right = BinaryTree(value - value // 2, None, toSplit)
		return True

	def reduce(self):
		while True:
			while self.explode():
				pass
			if not self.split():
				break

	def computeMagnitude(self):
		if self.right == None:
			return self.left
		return 3 * self.left.computeMagnitude() + 2 * self.right.computeMagnitude()


def getFileContent(path):
	with open(path, "r") as file:
		return file.read()

def getClosingIdx(string, start):
	assert string != '' and string[0] == '[', 'Invalid string: %s' % string
	count = 0
	for i in range(start, len(string)):
		if string[i] == '[':
			count += 1
		if string[i] == ']':
			count -= 1
		if count == 0:
			return i + 1
	return -1

def sumLines(lines):
	bt = BinaryTree.fromString(lines[0])
	for line in lines[1:]:
		bt = BinaryTree.fusion(bt, BinaryTree.fromString(line))
		bt.reduce() # must be done after each sum!
	return bt

# inputData = getFileContent('resources/example_18.txt')
inputData = getFileContent('resources/input_18.txt')

lines = [ line for line in inputData.split('\n') if line != '' ]

bt = sumLines(lines)
print('Sum of inputs:', bt.toString())

magnitude = bt.computeMagnitude()
print('\nMagnitude:', magnitude) # 3892

# ------------------------------------------
# Part 2:

# Testing all i != j, since 'addition' isn't commutative:
def getMaxMagnitude(lines):
	precomputedTrees = [ BinaryTree.fromString(line) for line in lines ]
	maxMagnitude = 0
	for i in range(len(lines)):
		for j in range(len(lines)):
			if i == j:
				continue
			bt = BinaryTree.fusion(precomputedTrees[i], precomputedTrees[j])
			bt.reduce() # must be done after each sum!
			maxMagnitude = max(maxMagnitude, bt.computeMagnitude())
	return maxMagnitude

maxMagnitude = getMaxMagnitude(lines)
print('\nMax magnitude:', maxMagnitude) # 4909 in 2.1 sec
