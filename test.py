from collections import Counter


chat_words = [("приветик", 10), ("приветик", 5)]


words_count = {}

for word, count in chat_words:
        words_count[word] = words_count.get(word, 0) + count


print(words_count)