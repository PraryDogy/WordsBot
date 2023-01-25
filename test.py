with open ('txt_food.txt', 'r') as file:
    food_list = file.read().split('\n')

food = ', '.join(random.sample(food_list, 5))
