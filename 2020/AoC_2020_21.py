import copy

print("\nPart 1:\n")

def get_lines(filename):
	file = open(filename, 'r')
	lines = file.read().splitlines()
	file.close()
	# print(lines)
	return lines

# filename = "resources/example_21"
filename = "resources/input_21"

lines = get_lines(filename)

def parse(line):
	i = line.index(" (contains ")
	return set(line[ : i].split(" ")), set(line[i+11 : -1].split(", "))

recipes = list(map(parse, lines))

print("\nrecipes:", len(recipes), "\n")
# for recipe in recipes:
# 	print(recipe)

def get_ingr_allerg():
	ingredients, allergens = [], []
	for recipe in recipes:
		ingredients.extend(recipe[0])
		allergens.extend(recipe[1])
	# Sorted to have a consistent list between runs:
	ingredients = sorted(list(set(ingredients)))
	allergens = sorted(list(set(allergens)))
	return ingredients, allergens

ingredients, allergens = get_ingr_allerg()

print("\ningredients:", len(ingredients), "\n")
# for ingredient in ingredients:
# 	print(ingredient)

print("\nallergens:", len(allergens), "\n")
# for allergen in allergens:
# 	print(allergen)


def get_constraints():
	candidate_sets = [0] * len(allergens)
	for i in range(len(allergens)):
		candidate_sets[i] = (allergens[i], set())
		for recipe in recipes:
			# print(i, allergens[i], recipe[1])
			if allergens[i] in recipe[1]:
				if len(candidate_sets[i][1]) == 0:
					candidate_sets[i] = (allergens[i], recipe[0])
				else:
					candidate_sets[i] = (allergens[i], candidate_sets[i][1].intersection(recipe[0]))
	candidate_sets = sorted(candidate_sets, key=lambda c : len(c[1]))
	return candidate_sets

constraints = get_constraints()
print("\nconstraints:\n\n", constraints, "\n")


# Could be more than one solution...
def build_ONE_solution():
	used_ingr_list, found_pairs = [], []
	has_changed = True
	while has_changed and len(found_pairs) < len(constraints):
		has_changed = False
		for constraint in constraints:
			allerg, ingr_list = constraint
			free_ingredients = list(filter(lambda ingr : not ingr in used_ingr_list, ingr_list))
			if free_ingredients == []:
				continue
			elif len(free_ingredients) == 1:
				chosen_ingr = free_ingredients[0]
				found_pairs.append((allerg, chosen_ingr))
				used_ingr_list.append(chosen_ingr)
				has_changed = True
	if len(found_pairs) < len(constraints):
		print("Failure, no solution found...")
		return None
	return found_pairs

solution = build_ONE_solution()
print("A solution:\n\n", solution)


result = 0
recipes_copy = copy.deepcopy(recipes)
for key in solution:
	allerg, ingr = key
	for recipe in recipes_copy:
		recipe[0].discard(ingr)

for recipe in recipes_copy:
	result += len(recipe[0])
print("\nresult:", result, "\n")


print("\nPart 2:\n")

sorted_sol = sorted(solution)
print(sorted_sol)

answer = ""
for key in sorted_sol:
	answer += key[1] + ","
answer = answer[: -1]
print("\nanswer:", answer)
