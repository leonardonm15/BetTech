import json

roulettes_needed = ["Roulette", "Football Roulette", "Hindi Roulette", "Speed Roulette", "Greek Roulette",
                    "Turkish Roulette", "Roleta Brasileira", "Prestige Roulette", "Nederlandstalige Roulette",
                    "Deutsches Roulette", "UK Roulette", "Bucharest Roulette", "Roulette Italiana"]

data = {}

for roulette in roulettes_needed:
    roulette_obj = {
        "patterns": {
            "rua": [0 for _ in range(12)],
            "canto": [[0 for _ in range(11)] for _ in range(2)]
        },
        "numbers": []
    }
    data[roulette] = roulette_obj

print(data)

with open("data.JSON", "w") as write_file:
    json.dump(data, write_file, indent=4)

