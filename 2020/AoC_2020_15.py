# Pretty version, using a class.

print("\nPart 1:\n")

class Game:
	def __init__(self, starting_list):
		init_size = 10000 # arbitrary
		self.hash_map = [(0, 0, 0)] * init_size # hash_map: key -> (count, age1, age2)
		self.current_epoch = 1
		n = len(starting_list)
		for i in range(n):
			self.add(starting_list[i])

	def print(self):
		print("hash_map:", self.hash_map[0 : 100]) # 100 first values
		print("current_epoch:", self.current_epoch)
		print("last_value:", self.last_value)

	def add(self, value):
		while value >= len(self.hash_map):
			self.hash_map.extend([(0, 0, 0)] * len(self.hash_map)) # doubling the size!
		count, age1, age2 = self.hash_map[value]
		self.hash_map[value] = (count + 1, age2, self.current_epoch)
		self.current_epoch += 1
		self.last_value = value

	def next(self):
		count, age1, age2 = self.hash_map[self.last_value]
		if count == 1:
			new_value = 0
		else:
			new_value = age2 - age1
		# print("epoch:", self.current_epoch, "choosing:", new_value)
		self.add(new_value)
		return new_value

def find_nth(nth, starting_list):
	game = Game(starting_list)
	for i in range(nth - len(starting_list)):
		game.next()
	result = game.last_value
	print(result)
	return result

result = find_nth(2020, [0, 13, 1, 8, 6, 15])


print("\nPart 2:\n")

result = find_nth(30000000, [0, 13, 1, 8, 6, 15]) # ~ 26 sec
