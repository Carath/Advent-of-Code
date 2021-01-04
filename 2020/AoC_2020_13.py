import math

print("\nPart 1:\n")

def get_lines(filename):
	file = open(filename, 'r')
	lines = file.read().splitlines()
	file.close()
	# print(lines)
	return lines

# filename = "resources/example_13"
filename = "resources/input_13"

lines = get_lines(filename)
print(lines)

def get_data(lines):
	start_time = int(lines[0])
	values = lines[1].split(',')
	bus_data_list = []
	for i in range(len(values)):
		if values[i] != "x":
			bus_data_list.append((i, int(values[i])))
	return start_time, bus_data_list

start_time, bus_data_list = get_data(lines)
print(start_time, bus_data_list)


def compute_waiting_time(start_time, bus_id):
	return bus_id * math.ceil(start_time / bus_id) - start_time

def find_earliest_bus(start_time, bus_data_list):
	time_list = map(lambda bus_data : (bus_data[1], compute_waiting_time(start_time, bus_data[1])), bus_data_list)
	return min(time_list, key=(lambda t : t[1]))

best_id, time = find_earliest_bus(start_time, bus_data_list)
print(best_id, time)
print("\nresult:", best_id * time)


print("\nPart 2:\n")

def check_validity(t):
	for (offset, bus_id) in bus_data_list:
		if (t + offset) % bus_id != 0:
			return False
	return True

def brute_force(bus_data_list):
	first_id, t = bus_data_list[0][1], 0
	while not check_validity(t):
		t += first_id
	return t

# print("result:", brute_force(bus_data_list)) # too slow for the input!

def pgcd(a, b):
	if b == 0:
		return a;
	else:
		return pgcd(b, a % b);

def bezout_coeffs(a, b):
	x, y = a, b
	l = []
	i = 0
	while y != 0:
		p = x // y
		r = x % y
		x = y
		y = r
		l.append((p, r))
		i += 1
	# print(l)
	u, v = 1, l[i - 2][0] # i >= 2, always.
	if i % 2 == 1:
		u, v = -u, -v
	while i > 2:
		temp = u
		u = v
		v = l[i - 3][0] * v + temp
		i -= 1
	return (u, -v)

print(bezout_coeffs(8, 5)) # ok
print(bezout_coeffs(8, 13)) # ok

def chinese(a, n, b, m):
	d = pgcd(n, m)
	if d != 1:
		print("Not coprimes:", n, m)
		return -1
	u, v = bezout_coeffs(n, m)
	return (b * u * n + a * v * m) % (n * m)

print(chinese(1, 5, 3, 7)) # ok

def chinese_full(a_n_list):
	a0, n0 = a_n_list[0]
	for i in range(1, len(a_n_list)):
		a, n = a_n_list[i]
		a0, n0 = chinese(a0, n0, a, n), n0 * n
	return a0

print(chinese_full([(0, 2), (1, 5), (3, 7)])) # ok

chinese_input = [bus_data_list[0]] + list(map(lambda c : (c[1] - c[0], c[1]), bus_data_list[1 : ]))
print(chinese_input)
print("\nresult:", chinese_full(chinese_input))
