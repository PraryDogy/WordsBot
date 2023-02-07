# from . import json
import json


__all__ = (
    "ducks",
    "food",
    "puppies_words",
    "puppies_url",
    "penis_names",
    "ass_names",
    "stop_words",
    "destiny_questions",
    "destiny_answers",
    "pokemons",
    "khalisi_words"
)

with open("dicts/ducks.txt", "r") as file:
    ducks_url: list = file.read().split('\n')

ducks_num = [
    *(str(i) for i in range(1, 16)),
    "16, 17, 18",
    *(str(i) for i in range(19, 56)),
    "56, 57, 58",
    *(str(i) for i in range(59, 93)),
    "93, 94",
    *(str(i) for i in range(95, 102)),
    "102, 103",
    *(str(i) for i in range(104, 125)),
    ]

ducks = {
    url: num
    for url, num in zip(ducks_url, ducks_num)
        }

with open ("dicts/food.txt", "r") as file:
    food: list = file.read().split('\n')

with open("dicts/puppies_words.txt", "r") as file:
    puppies_words: list = file.read().split("\n")

with open("dicts/puppies_url.txt", "r") as file:
    puppies_url: list = file.read().split("\n")

with open("dicts/penises.txt", "r") as file:
    penis_names: list = file.read().split("\n")

with open("dicts/ass.txt", "r") as file:
    ass_names: list = file.read().split("\n")

with open("dicts/stop_words.txt", "r") as file:
    stop_words: list = file.read().split("\n")

with open("dicts/destiny_answers.txt", "r") as file:
    destiny_answers: list = file.read().split("\n")

with open("dicts/destiny_questions.txt", "r") as file:
    destiny_questions: list = file.read().split("\n")

with open("dicts/pokemons.txt", "r") as file:
    pokemons: dict = json.loads(file.read())

with open("dicts/khalisi.txt", "r") as file:
    khalisi_words: dict = json.loads(file.read())
