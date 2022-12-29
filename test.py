def sort_words(input: tuple):
    unic_words = set(i[0] for i in input)
    result = []
    for word in unic_words:
        counter = 0
        for w, c in input:
            counter += c if word == w else False
        result.append((word, counter))
    return tuple(reversed(sorted(result, key=lambda x: x[1])))


tst = (('это', 3), ('это', 1), ('какое-то слово', 1), ('это', 2), ('другое слово', 3))
print(sort_words(tst))