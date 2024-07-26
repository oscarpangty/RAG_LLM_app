import ollama

res = ollama.chat(
	model="llava",
	messages=[
		{
			'role': 'user',
			'content': 'Describe this image:',
			'images': ['C:/Users/oscar/Desktop/chumei_station/oyster.jpg']
		}
	]
)

print(res['message']['content'])