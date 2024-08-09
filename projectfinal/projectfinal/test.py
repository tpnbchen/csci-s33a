from random import shuffle
COLORS = ("white", "yellow", "green", "blue", "red")
NUMBERS = 5
players = ["a", "b"]

deck = []
for color in COLORS:
    for i in range(1, NUMBERS):
        if i == 1:
            for j in range(3):
                deck.append({'color': color, "number": f"{i}"})
        elif i in [2, 3, 4]:
            for j in range(2):
                deck.append({'color': color, "number": f"{i}"})
        else:
            deck.append({'color': color, "number": f"{i}"})
shuffle(deck)


hands = {}
if len(players) in [4, 5]:
    handsize = 4
else:
    handsize = 5
for player in players:
    hands[player] = {}
    for i in range(1, handsize+1):
        card = f"card {i}"
        hands[player].update({card: deck.pop()})
        hands[player][card].update({"knowledge": set()})
print(hands)