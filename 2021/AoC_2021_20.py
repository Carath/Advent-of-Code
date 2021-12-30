def getFileContent(path):
	with open(path, "r") as file:
		return file.read()

# inputData = getFileContent('resources/example_20.txt')
inputData = getFileContent('resources/input_20.txt')
print('inputData:\n\n', inputData)

inputData = inputData.split('\n\n')
enhancementAlgorithm = [ int(c == '#') for c in inputData[0] ]

# Formatting the image as a matrix:
inputImage = [ list(s) for s in inputData[1].split('\n') if s != '' ]
inputImage = [ [ int(c == '#') for c in row ] for row in inputImage ]

def printImage(image, title=''):
	print(title)
	for row in image:
		print(''.join([ '#' if val == 1 else '.' for val in row ]))
	print()

print('enhancementAlgorithm:\n\n', enhancementAlgorithm)
printImage(inputImage, title='\nInput image:\n')

def getWindowValue(image, targetRow, targetCol, backgroundValue):
	rowsRange, colsRange = range(len(image)), range(len(image[0]))
	windowRange, s = range(-1, 2), 0
	for row in windowRange:
		for col in windowRange:
			val = backgroundValue
			if targetRow + row in rowsRange and targetCol + col in colsRange:
				val = image[targetRow + row][targetCol + col]
			s = 2 * s + val
	return s

# Careful: background may alternate between being lit and dark!
def enhanceImage(enhancementAlgorithm, image, backgroundValue=0):
	output = [ [0] * (len(image[0])+2) for row in range(len(image)+2) ]
	for row in range(len(output)):
		for col in range(len(output[0])):
			output[row][col] = enhancementAlgorithm[getWindowValue(image, row-1, col-1, backgroundValue)]
	backgroundValue = enhancementAlgorithm[-backgroundValue]
	return output, backgroundValue

def enhancement(enhancementAlgorithm, image, steps, backgroundValue=0, verbose=False):
	for step in range(steps):
		image, backgroundValue = enhanceImage(enhancementAlgorithm, image, backgroundValue)
		if verbose:
			printImage(image, title='Image after step %d:\n' % (step+1))
	return image, backgroundValue

# Ignoring infinite background which may be lit - count only relevant for even steps number:
def countLitPixels(image):
	count = 0
	for row in image:
		for col in row:
			count += col
	return count

enhancedImage, backgroundValue = enhancement(enhancementAlgorithm, inputImage, 2, backgroundValue=0, verbose=True)

litPixelsNumber = countLitPixels(enhancedImage)
print('\nLit pixels number:', litPixelsNumber) # 5349

# ------------------------------------------
# Part 2:

enhancedImage, backgroundValue = enhancement(enhancementAlgorithm, enhancedImage, 48, backgroundValue)

litPixelsNumber = countLitPixels(enhancedImage)
print('\nLit pixels number:', litPixelsNumber) # 15806 in 3.8s
