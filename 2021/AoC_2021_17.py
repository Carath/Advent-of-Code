# inputData = 'target area: x=20..30, y=-10..-5'
inputData = 'target area: x=102..157, y=-146..-90'

bounds = inputData.split('..')
bounds = [bounds[0].split('x=')[1]] + bounds[1].split(', y=') + [bounds[-1]]
bounds = [ int(val) for val in bounds ]
print('bounds:', bounds)

def run(vx0, vy0, bounds):
	# print('Init:', vx0, vy0)
	xmin, xmax, ymin, ymax = bounds[0], bounds[1], bounds[2], bounds[3]
	x, y, vx, vy, step, maxHeight = 0, 0, vx0, vy0, 0, 0
	while x <= xmax and y >= ymin: # works since xmax > 0 and ymin < 0
		if x >= xmin and y <= ymax:
			# print('Hit at step:', step)
			return True, maxHeight
		step += 1
		x += vx
		y += vy
		maxHeight = max(maxHeight, y)
		if vx > 0:
			vx -= 1
		elif vx < 0:
			vx += 1
		vy -= 1
	# print('Failure after %d steps' % step)
	return False, 0

def findAllValidInit(bounds):
	validInits, globalMaxHeight = [], 0
	maxValX, maxValY = bounds[1] + 1, max(abs(bounds[2]), abs(bounds[3])) + 1
	for vx0 in range(0, maxValX):
		for vy0 in range(-maxValY, maxValY):
			success, maxHeight = run(vx0, vy0, bounds)
			if success:
				validInits.append((vx0, vy0))
				globalMaxHeight = max(globalMaxHeight, maxHeight)
	return validInits, globalMaxHeight

validInits, globalMaxHeight = findAllValidInit(bounds)
print('\nMax height:', globalMaxHeight, '\n') # 10585

# ------------------------------------------
# Part 2:

print('Valid inits number:', len(validInits)) # 5247
