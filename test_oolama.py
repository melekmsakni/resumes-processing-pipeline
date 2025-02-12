# import ollama
# response = ollama.chat(model='llama3.1', messages=[
#   {
#     'role': 'user',
#     'content': 'Why is the sky blue?',
#   },
# ])


from ollama import Client
client = Client(host='http://localhost:8006')
response = client.chat(model='llama3.1', messages=[
  {
    'role': 'user',
    'content': 'hey',
  },
])
print(response['message']['content'])