from chatgpt_wrapper import ChatGPT

bot = ChatGPT()
# return the full result
response = bot.ask("Когда вымерли динозавры?")
print(response)

# # return the result in streaming (chunks)
# for chunk in bot.ask_stream("tell me a story about cats and dogs"):
#     print(chunk)