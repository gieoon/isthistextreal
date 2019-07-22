import os, json
import pandas as pd
import random
from random import randrange
import flask

path = 'data/'
generatedData = []
json_files = [f for f in os.listdir(path) if f.endswith('.jsonl')]
for index, js in enumerate(json_files):
	print('loading file for GENERATED: ', js)
	for line in open(os.path.join(path, js), 'r'):
		json_text = json.loads(line)['text'];
		generatedData.append(json_text)

actualData = []
json_files = [f for f in os.listdir(path) if f.endswith('.jsonl_actual')]
for index, js in enumerate(json_files):
	print('loading file for ACTUAL: ', js)
	for line in open(os.path.join(path, js), 'r'):
		json_text = json.loads(line)['text'];
		actualData.append(json_text)

print('--- Loading datasets complete ---')



app = flask.Flask(__name__)

@app.route("/")
def home():
	#get random texts from both generated and actual
	#generated_txt = random.choice(generatedData)
	#actual_txt = random.choice(actualData)
	output_txt = ''
	is_actual = randrange(0, 2)

	if(is_actual):
		print('is_actual: ', is_actual)
		output_txt = random.choice(actualData)
	else:
		output_txt = random.choice(generatedData)
	return flask.render_template('index.html', txt=output_txt, is_actual=is_actual)
	#return flask.render_template('index.html', actual_txt = actual_txt, generated_txt = generated_txt)

if __name__ == "__main__":
	app.run(debug=False)



'''
json_structure = pd.DataFrame(columns=['text'])
print(json_structure.head(5))
for index, js in enumerate(json_files):
	with open(os.path.join(path, js)) as json_file:
		print('reading from: ', json_file)
		json_text = json.load(json_file)
		print(json_text)
'''