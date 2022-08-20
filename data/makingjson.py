import json

roulettes_needed = ["Roulette", "Football Roulette", "Hindi Roulette", "Speed Roulette", "Greek Roulette",
                    "Turkish Roulette", "Roleta Brasileira", "Prestige Roulette", "Nederlandstalige Roulette",
                    "Deutsches Roulette", "UK Roulette", "Bucharest Roulette", "Roulette Italiana"]

data = {}
print(roulettes_needed)
for roulette in roulettes_needed:
    roulette_obj = {
        "patterns": {
            "direta": [0 for _ in range(37)],
            "rua": [0 for _ in range(12)],
            "rua_dupla": [0 for _ in range(11)],
            "canto": [[0 for _ in range(11)] for _ in range(2)],
            "dupla": {
                "right": [[0 for _ in range(11)] for _ in range(3)],
                "down": [[0 for _ in range(12)] for _ in range(2)]
            }
        },
        "avisos": {
            "direta": [0 for _ in range(37)],
            "rua": [0 for _ in range(12)],
            "rua_dupla": [0 for _ in range(11)],
            "canto": [[0 for _ in range(11)] for _ in range(2)],
            "dupla": {
                "right": [[0 for _ in range(11)] for _ in range(3)],
                "down": [[0 for _ in range(12)] for _ in range(2)]
            }
        },
        "numbers": [-1 for _ in range(10)]
    }
    data[roulette] = roulette_obj

with open("data/data.JSON", "w") as write_file:
    json.dump(data, write_file, indent=4)

