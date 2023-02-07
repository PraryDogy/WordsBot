import json


__all__ = (
    "ducks_url",
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

with open("dicts/ducks_url.json", "r") as file:
    ducks_url: dict = json.loads(file.read())

with open ("dicts/food.json", "r") as file:
    food: list = json.loads(file.read())

with open("dicts/puppies_words.json", "r") as file:
    puppies_words: list = json.loads(file.read())

with open("dicts/puppies_url.json", "r") as file:
    puppies_url: list = json.loads(file.read())

with open("dicts/penis_names.json", "r") as file:
    penis_names: list = json.loads(file.read())

with open("dicts/ass_names.json", "r") as file:
    ass_names: list = json.loads(file.read())

with open("dicts/stop_words.json", "r") as file:
    stop_words: list = json.loads(file.read())

with open("dicts/destiny_answers.json", "r") as file:
    destiny_answers: list = json.loads(file.read())

with open("dicts/destiny_questions.json", "r") as file:
    destiny_questions: list = json.loads(file.read())

with open("dicts/pokemons.json", "r") as file:
    pokemons: dict = json.loads(file.read())

with open("dicts/khalisi_words.json", "r") as file:
    khalisi_words: dict = json.loads(file.read())

