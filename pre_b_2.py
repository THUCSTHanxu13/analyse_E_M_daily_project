import os
import re
import json

tags_M = {}
f = open("M_tags.txt", "r")
for i in f.readlines():
	nam, uid = i.strip().split("\t")
	tags_M[nam.strip().lower()] = (int)(uid.strip())
f.close()

tags_E = {}
f = open("E_tags.txt", "r")
for i in f.readlines():
	nam, uid = i.strip().split("\t")
	tags_E[nam.strip()] = (int)(uid.strip())
f.close()


def work_M(file_name):
	print (file_name)
	data = []
	f = open('./results/' + file_name, 'r')
	last_tag = ""
	s = 0
	while True:
		content = f.readline()
		s = s + 1
		print (s)
		if content == "":
			break

		content = content.strip()
		if content == "":
			continue

		if re.search('<\d+>', content):
			data.append({})
			last_tag = ""
			continue

		if content.lower() in tags_M:
			data[-1][content.lower()] = ""
			last_tag = content.lower()
			continue

		if len(data) != 0 and last_tag != "":
			data[-1][last_tag] += "\n" + content
	f.close()

	f = open('./jsons/' + file_name, 'w')
	f.write(json.dumps(data))
	f.close()


def work_E(file_name):
	print (file_name)
	data = []
	f = open('./results/' + file_name, 'r')
	last_tag = ""
	s = 0
	while True:
		content = f.readline()
		if content == "":
			break

		content = content.strip()
		if content == "":
			continue

		if re.search('RECORD[\s]*?\d+', content):
			data.append({})
			last_tag = ""
			continue

		if (content.find('ORIGINAL (NON-ENGLISH) TITLE')!=-1) and (not 'TITLE' in data[-1]):
			content = content.replace('ORIGINAL (NON-ENGLISH) TITLE', "TITLE")

		if content in tags_E:
			data[-1][content] = ""
			last_tag = content
			continue

		if len(data) != 0 and last_tag != "":
			data[-1][last_tag] += "\n" + content
	f.close()

	f = open('./jsons/' + file_name, 'w')
	f.write(json.dumps(data))
	f.close()


file_list = os.listdir("./results/")
for file_name in file_list:
	# if file_name.find("M") != -1:
	# 	work_M(file_name.strip())
	# file_name = "40-E.txt"
	if file_name.find("E") != -1:
		work_E(file_name.strip())
	# break

# f = open("jsons/62-E.txt", "r")
# content = json.loads(f.read())
# print (len(content))
# for i in content:
# 	print (i)
# 	for j in i:
# 		print (j)
# f.close()