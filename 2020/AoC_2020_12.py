print("\nPart 1:\n")

def get_lines(filename):
	file = open(filename, 'r')
	lines = file.read().splitlines()
	file.close()
	# print(lines)
	return lines

# filename = "resources/example_12"
filename = "resources/input_12"

lines = get_lines(filename)
lines = list(map(lambda line : (line[0], int(line[1 : ])), lines))
# print(lines)


def manhattan_dist(x, y):
	return abs(x) + abs(y)

def rotate(x, y, angle):
	r = (angle / 90) % 4 # quarter turn
	if r == 0:
		return (x, y)
	elif r == 1:
		return (-y, x)
	elif r == 2:
		return (-x, -y)
	else:
		return (y, -x)

def follow_path(lines):
	dir_x, dir_y = 1, 0
	x, y = 0, 0
	for line in lines:
		direction = line[0]
		value = line[1]
		if direction == 'N':
			y += value
		elif direction == 'S':
			y -= value
		elif direction == 'E':
			x += value
		elif direction == 'W':
			x -= value
		elif direction == 'F':
			x += dir_x * value
			y += dir_y * value
		elif direction == 'L':
			dir_x, dir_y = rotate(dir_x, dir_y, value)
		else: # direction == 'R'
			dir_x, dir_y = rotate(dir_x, dir_y, -value)
	print(x, y)
	return manhattan_dist(x, y)

print("result:", follow_path(lines))


print("\nPart 2:\n")

def follow_path_2(lines):
	waypoint_x, waypoint_y = 10, 1
	x, y = 0, 0
	for line in lines:
		direction = line[0]
		value = line[1]
		if direction == 'N':
			waypoint_y += value
		elif direction == 'S':
			waypoint_y -= value
		elif direction == 'E':
			waypoint_x += value
		elif direction == 'W':
			waypoint_x -= value
		elif direction == 'F':
			x += waypoint_x * value
			y += waypoint_y * value
		elif direction == 'L':
			waypoint_x, waypoint_y = rotate(waypoint_x, waypoint_y, value)
		else: # direction == 'R'
			waypoint_x, waypoint_y = rotate(waypoint_x, waypoint_y, -value)
	print(x, y)
	return manhattan_dist(x, y)

print("result:", follow_path_2(lines))
