# split the large 600MB file into subsets of smaller ones that are 30MB each.
import os, json

#print(txt)

count = 1
file_count = 1
f = open('split_data/webtext.train.' + str(file_count) + '.jsonl', 'w+', encoding='utf8')

for line in open('data/webtext.train.jsonl_actual_ignore', 'r'):
	json_text = json.loads(line)#['text'];
	#f.write('{"text":"' + json_text + '"}')
	f.write(json.dumps(json_text) + '\n')
	count += 1
	if count > 2500:
		print('writing to new: ', file_count)
		f.close()
		file_count += 1
		count = 0
		f = open('split_data/webtext.train.' + str(file_count) + ".jsonl", "w+", encoding='utf8')

