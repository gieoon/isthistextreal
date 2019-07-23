import os, json
import random
from random import randrange
import flask
#import urllib
import logging
import threading

app = flask.Flask(__name__)

class global_data:
	generated_data1 = []
	generated_data2 = []
	generated_data3 = []
	actual_data1 = []
	actual_data2 = []
	actual_data3 = []
	count_actual = 0
	count_generated = 0
	load_array_no_actual = 0 # Start at 0 to init
	load_array_no_generated = 0 # Start at 0 to init
	current_array_no_actual = 1
	current_array_no_generated = 1
	SIZE_LIMIT = 500
	EXTERNAL_DATASETS_COUNT = 103 # last two datasets are webtext.test & webtext.valid

g = global_data()

def getNextArray(is_actual):
	if is_actual:
		g.load_array_no_actual += 1
		if g.load_array_no_actual == 4:
			g.load_array_no_actual = 1

		if g.load_array_no_actual == 1:
			g.actual_data1 = []
			return g.actual_data1
		elif g.load_array_no_actual == 2:
			g.actual_data2 = []
			return g.actual_data2
		else:
			g.actual_data3 = []
			return g.actual_data3
	else:
		g.load_array_no_generated += 1
		if g.load_array_no_generated == 4:
			g.load_array_no_generated = 1

		if g.load_array_no_generated == 1:
			g.generated_data1 = []
			return g.generated_data1
		elif g.load_array_no_generated == 2:
			g.generated_data2 = []
			return g.generated_data2
		else:
			g.generated_data3 = []
			return g.generated_data3

def getCurrentArray(is_actual):
	if is_actual:
		if g.current_array_no_actual == 1:
			return g.actual_data1
		elif g.current_array_no_actual == 2:
			return g.actual_data2
		else:
			return g.actual_data3
	else:
		if g.current_array_no_generated == 1:
			return g.generated_data1
		elif g.current_array_no_generated == 2:
			return g.generated_data2
		else:
			return g.generated_data3

def loadNextArrayInBackground(is_actual):
	filename = ''
	if is_actual :
		filename = 'split_data/webtext.train.' + str(randrange(1, g.EXTERNAL_DATASETS_COUNT)) + '.jsonl'
	else:
		filename = 'data/' + random.choice(os.listdir('data/'))

	next_array = getNextArray(is_actual)
	for line in open(filename, 'r'):
		text = json.loads(line)['text']
		next_array.append(text)
	print('next array loaded: ' + str(len(next_array)))

# Initialize for current
loadNextArrayInBackground(True)
loadNextArrayInBackground(False)
# Initialize for next
loadNextArrayInBackground(True)
loadNextArrayInBackground(False)
# Initialize for last
loadNextArrayInBackground(True)
loadNextArrayInBackground(False)
# Reset to next
g.load_array_no_actual = 2
g.load_array_no_generated = 2

@app.route('/')
def home():
	#get random texts from both generated and actual
	output_txt = ''
	is_actual = randrange(0, 2)
	print('================================================================')
	print('g.count_actual: ' + str(g.count_actual))
	print('g.count_generated: ' + str(g.count_generated))
	print('g.current_array_no_actual: ' + str(g.current_array_no_actual))
	print('g.current_array_no_generated: ' + str(g.current_array_no_generated))
	print('g.load_array_no_actual: ' + str(g.load_array_no_actual))
	print('g.load_array_no_generated: ' + str(g.load_array_no_generated))
	if(g.count_actual == g.SIZE_LIMIT):
		g.count_actual = 0
		print('loading next ACTUAL array')
		t = threading.Thread(target=loadNextArrayInBackground, args=[is_actual])
		t.start()
		print('thread ACTUAL finished')
		g.current_array_no_actual += 1
		if g.current_array_no_actual == 4:
			g.current_array_no_actual = 1
	elif(g.count_generated == g.SIZE_LIMIT):
		g.count_generated = 0
		print('loading next GENERATED array')
		t = threading.Thread(target=loadNextArrayInBackground, args=[is_actual])
		t.start()
		print('thread GENERATED finished')
		g.current_array_no_generated += 1
		if g.current_array_no_generated == 4:
			g.current_array_no_generated = 1

	#print('is_actual: ', is_actual)
	if(is_actual):
		g.count_actual += 1
		#logging.info('is_actual: ', is_actual)
	else:
		g.count_generated += 1
		#print('generated_data: ', generated_data)
	array = getCurrentArray(is_actual)
	if len(array) > 0:
		output_txt = random.choice(array)
	else:
		return flask.render_template('wait.html')

	return flask.render_template('index.html', txt=output_txt, is_actual=is_actual)

@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500

if __name__ == "__main__":
	app.run(debug=True)

# Generating from Google Storage URL's
'''
generated_data = []
actual_data = []

for split in ['valid', 'test', 'train']:
	filename = split + ".jsonl"
	url = "https://storage.googleapis.com/gpt-2/output-dataset/v1/webtext." + filename
	logging.info('Loaded ' + url)
	response = urllib.urlopen(url)
	for line in response:
		text = json.loads(line)['text']
		actual_data.append(text)

for ds in [
    'small-117M',  'small-117M-k40',
    'medium-345M', 'medium-345M-k40',
    'large-762M',  'large-762M-k40',
    'xl-1542M',    'xl-1542M-k40',
]:
    for split in ['valid', 'test']: #'train', 
        filename = ds + "." + split + '.jsonl'
        url = "https://storage.googleapis.com/gpt-2/output-dataset/v1/" + filename
        logging.info('Loaded ' + url)
        response = urllib.urlopen(url)
        for line in response:
        	text = json.loads(line)['text']
        	generated_data.append(text)

for url in [
	'https://storage.googleapis.com/gpt-2/output-dataset/v1/webtext.test.jsonl',
	'https://storage.googleapis.com/gpt-2/output-dataset/v1/webtext.valid.jsonl',
	'https://storage.googleapis.com/gpt-2/output-dataset/v1/webtext.train.jsonl'
]:
'''

# Loading all from local filesystem
'''
path = 'data/'
json_files = [f for f in os.listdir(path) if f.endswith('.jsonl')]
for index, js in enumerate(json_files):
	print('loading file for GENERATED: ', js)
	for line in open(os.path.join(path, js), 'r'):
		json_text = json.loads(line)['text'];
		generated_data.append(json_text)


json_files = [f for f in os.listdir(path) if f.endswith('.jsonl_actual')]
for index, js in enumerate(json_files):
	print('loading file for ACTUAL: ', js)
	for line in open(os.path.join(path, js), 'r'):
		json_text = json.loads(line)['text']
		actual_data.append(json_text)

path = 'split_data/'
json_files = [f for f in os.listdir(path) if f.endswith('.jsonl')]
for index, js in enumerate(json_files):
	print('loading file for ACTUAL: ', js)
	for line in open(os.path.join(path, js), 'r'):
		#line = line.decode("utf-8")
		json_text = json.loads(line)['text']
		#print(json_text)
		actual_data.append(json_text)

logging.info('--- Loading datasets complete ---')
print('--- Loading datasets complete ---')
'''

