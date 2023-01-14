import random
import math


def gold_chance():
    chance = 0.05
    return bool(math.floor(random.uniform(0, 1/(1-chance))))


print()
print(gold_chance())
print()