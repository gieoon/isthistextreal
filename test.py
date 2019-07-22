import urllib
import os, json

response = urllib.urlopen('https://storage.googleapis.com/gpt-2/output-dataset/v1/webtext.test.jsonl')
#print(txt)
for line in response:
	json_text = json.loads(line)['text'];
	print(json_text)
	input()
