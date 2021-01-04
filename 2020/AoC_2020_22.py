print("\nPart 1:\n")

def get_lines(filename):
	file = open(filename, 'r')
	lines = file.read().splitlines()
	file.close()
	# print(lines)
	return lines

# filename = "resources/example_22"
filename = "resources/input_22"

lines = get_lines(filename)

def get_cards():
	cards_player_1, cards_player_2, i = [], [], 0
	for line in lines:
		if line == "":
			i += 1
		elif line[: 6] == "Player":
			continue
		elif i == 0:
			cards_player_1.append(int(line))
		else:
			cards_player_2.append(int(line))
	return cards_player_1, cards_player_2

cards_player_1, cards_player_2 = get_cards()
print(cards_player_1)
print(cards_player_2)

def game(cards_player_1, cards_player_2):
	new_cards_1, new_cards_2 = cards_player_1[:], cards_player_2[:]
	game_round, winner, score = 1, 0, 0
	while len(new_cards_1) > 0 and len(new_cards_2) > 0:
		# print("\n-- Round " + str(game_round) + " --")
		card_1, card_2 = new_cards_1[0], new_cards_2[0]
		if card_1 > card_2:
			new_cards_1 = new_cards_1[1 :] + [card_1] + [card_2]
			new_cards_2 = new_cards_2[1 :]
			# print("Player 1 wins the round!")
		else:
			new_cards_1 = new_cards_1[1 :]
			new_cards_2 = new_cards_2[1 :] + [card_2] + [card_1]
			# print("Player 2 wins the round!")
		game_round += 1
	# Computing the score:
	if len(new_cards_1) > 0: # Player 1 wins
		for i in range(len(new_cards_1)):
			score += new_cards_1[i] * (len(new_cards_1) - i)
		winner = 1
	else: # Player 2 wins
		for i in range(len(new_cards_2)):
			score += new_cards_2[i] * (len(new_cards_2) - i)
		winner = 2
	print("\ngame_round:", game_round - 1)
	print(new_cards_1)
	print(new_cards_2)
	return winner, score

result = game(cards_player_1, cards_player_2)
print("\nresult:", result)


print("\nPart 2:\n")

# depth must be 0 at the beginning.
def game_recursive(cards_player_1, cards_player_2, depth):
	new_cards_1, new_cards_2 = cards_player_1[:], cards_player_2[:]
	history_player_1, history_player_2 = [], []
	game_round, winner, score = 1, 0, 0
	while len(new_cards_1) > 0 and len(new_cards_2) > 0:

		if new_cards_1 in history_player_1 or new_cards_2 in history_player_2:
			winner = 1 # Stop this current game: player 1 wins!
			break

		history_player_1.append(new_cards_1)
		history_player_2.append(new_cards_2)
		card_1, card_2 = new_cards_1[0], new_cards_2[0]
		result_subgame = 0, 0

		if card_1 <= len(new_cards_1[1 :]) and card_2 <= len(new_cards_2[1 :]): # doing a subgame!
			result_subgame = game_recursive(new_cards_1[1 : card_1 + 1], new_cards_2[1 : card_2 + 1], depth + 1)

		if result_subgame[0] == 1 or (result_subgame[0] == 0 and card_1 > card_2):
			new_cards_1 = new_cards_1[1 :] + [card_1] + [card_2]
			new_cards_2 = new_cards_2[1 :]

		else:
			new_cards_1 = new_cards_1[1 :]
			new_cards_2 = new_cards_2[1 :] + [card_2] + [card_1]

		game_round += 1

	# Finding the winner:
	if winner == 1 or len(new_cards_1) > 0: # Player 1 wins
		winner = 1
	else: # Player 2 wins
		winner = 2

	# Computing the score:
	if depth == 0:
		if len(new_cards_1) > 0: # Player 1 wins
			for i in range(len(new_cards_1)):
				score += new_cards_1[i] * (len(new_cards_1) - i)
		else: # Player 2 wins
			for i in range(len(new_cards_2)):
				score += new_cards_2[i] * (len(new_cards_2) - i)

	# print("\ngame_round:", game_round - 1)
	return winner, score

result = game_recursive(cards_player_1, cards_player_2, 0)
print("\nresult:", result)
