print("\nPart 1:\n")

def get_lines(filename):
	file = open(filename, 'r')
	lines = file.read().splitlines()
	file.close()
	# print(lines)
	return lines

filename = "resources/input_18"

lines = get_lines(filename)
# print(lines)

class Node:

	def __init__(self, x, op = None, y = None):
		self.left = x
		self.op = op
		self.right = y

	def toString(self):
		if self.op == None: # its a leaf!
			return str(self.left)
		return '(' + self.left.toString() + ' ' + self.op + ' ' + self.right.toString() + ')'

node = Node(Node(Node(3), '+', Node(5)), '*', Node(2))
# print(node.toString())


# No side effects, returns a new string!
def cleanup(string):
	string = string.replace(' ', '')
	string = string.replace('+', ' + ')
	string = string.replace('-', ' - ')
	string = string.replace('*', ' * ')
	string = string.replace('(', '( ')
	string = string.replace(')', ' )')
	return string

def get_splitted(string):
	return cleanup(string).split(' ')

expressions = list(map(lambda line : get_splitted(line), lines))


# cleanup before splitting!
def get_subexpr_down(splitted, end):
	if splitted[end] != ')':
		return None, end - 1
	parenthesis_count = -1
	index = end - 1
	while index >= 0 and parenthesis_count < 0:
		if splitted[index] == '(':
			parenthesis_count += 1
		elif splitted[index] == ')':
			parenthesis_count -= 1
		index -= 1
	return splitted[index+2 : end], index

# cleanup before splitting!
def get_subexpr_up(splitted, start):
	if splitted[start] != '(':
		return None, start + 1
	parenthesis_count = 1
	index = start + 1
	while index < len(splitted) and parenthesis_count > 0:
		if splitted[index] == '(':
			parenthesis_count += 1
		elif splitted[index] == ')':
			parenthesis_count -= 1
		index += 1
	return splitted[start+1 : index-1], index

# splitted = get_splitted("  7+ (2* 32)   * (4 *(5 +  6))")
# print(splitted)
# print(get_subexpr_down(splitted, 16))
# print(get_subexpr_up(splitted, 2))


# Left to right priority!
def build_tree(splitted):
	try:
		end = len(splitted) - 1
		if splitted[end] == ')':
			sub_split, start = get_subexpr_down(splitted, end)
			if start < 0:
				return build_tree(sub_split)
			else:
				return Node(build_tree(splitted[ : start]), splitted[start], build_tree(sub_split))
		elif len(splitted) == 1:
			return Node(int(splitted[0]))
		else:
			return Node(build_tree(splitted[ : end-1]), splitted[end-1], Node(int(splitted[end])))
	except:
		print("Invalid expression\n")
		return Node(None)

def get_tree(string):
	return build_tree(get_splitted(string))

def compute(tree):
	try:
		if tree.op == None:
			return tree.left
		else:
			left_term = compute(tree.left)
			right_term = compute(tree.right)
			if tree.op == '+':
				return left_term + right_term
			elif tree.op == '-':
				return left_term - right_term
			elif tree.op == '*':
				return left_term * right_term
			else:
				print("Unsupported operation")
				return None
	except:
		print("Invalid expression\n")
		return None

def test(string):
	tree = get_tree(string)
	print(string, "\n->", tree.toString(), "\n =", compute(tree), "\n")


test("  7+ (2* 32)   * (4 *(5 +  6))")
# test("2 * 3 + (4 * 5)")
# test("5 + (8 * 3 + 9 + 3 * 4 * 3)")
# test("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))")
# test("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2")
# test("  7+ 2* 32)   * (4 *(5 +  6))") # invalid expression!

def compute_big_sum(expressions):
	result = 0
	for exp in expressions:
		tree = build_tree(exp)
		result += compute(tree)
	return result

print("result:", compute_big_sum(expressions))


print("\nPart 2:\n")

# + prioritized over *
def enforce_priority(splitted):
	i = 0
	while i < len(splitted):
		if splitted[i] == '+':
			left_term, j = get_subexpr_down(splitted, i - 1)
			left_right, k = get_subexpr_up(splitted, i + 1)
			splitted = splitted[ : j+1] + ['('] + splitted[j+1 : k] + [')'] + splitted[k : ]
			i += 2 # +2 to compensate adding a '('.
		else:
			i += 1
	return splitted

# string = "1 + (2 * 3) + 4 * 5 + 6"
# string = "1 + (2 * 3) + (4 * (5 + 6))"
# string = "2 * 3 + (4 * 5)"
# string = "5 + (8 * 3 + 9 + 3 * 4 * 3)"
# string = "5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))"
string = "((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2"

print(string)
tree = build_tree(enforce_priority(get_splitted(string)))
print(tree.toString())
print(compute(tree))
# All good man!

modified_expr = list(map(lambda line : enforce_priority(get_splitted(line)), lines))

print("result:", compute_big_sum(modified_expr))
