print("\nPart 1:\n")

def get_lines(filename):
	file = open(filename, 'r')
	lines = file.read().splitlines()
	file.close()
	# print(lines)
	return lines

filename = "resources/input_5"
lines = get_lines(filename)


def convert_to_binary(string):
	return list(map(lambda c : int(c == 'B' or c == 'R'), string))


def get_id(binary):
	n, power, number = len(binary), 1, 0
	for i in range(0, n):
		number += binary[n - 1 - i] * power
		power *= 2
	return number


binary = convert_to_binary("FBFBBFFRLR")
print(binary)

board_id = get_id(binary)
row, col = board_id >> 3, board_id % 8
print(board_id, row, col)

id_list = list(map(get_id, map(convert_to_binary, lines)))
highest_id = max(id_list)
print("\nhighest_id:", highest_id)


print("\nPart 2:\n")

def find_seat(id_list):
	hash_map_len = 1024 # 10 bits
	hash_map = [0] * hash_map_len
	for flight_id in id_list:
		hash_map[flight_id] = 1
	# print(hash_map)
	for i in range(1, hash_map_len - 1):
		if hash_map[i - 1] == 1 and hash_map[i] == 0 and hash_map[i + 1] == 1:
			return i
	return -1

seat = find_seat(id_list)
print("seat:", seat)
