#coding:utf-8
import re
import json
import os
from utils import *

def clear(text):
	text = convert_to_unicode(text)
	text = clean_text(text, True)
	text = tokenize_chinese_chars(text)
	text = re.sub('<.*?>', '', text)
	text = re.sub('&n.*?;', '', text)
	return text

def check(str1, str2):
	lists1 = str1.split()
	lists2 = str2.split()
	rate = 0.0
	hash = {}
	for i in lists1:
		if not i in hash:
			hash[i] = 0
		hash[i] += 1
	for j in lists2:
		if j in hash and hash[j]!=0:
			hash[j] -= 1
			rate += 1.0
	return (rate / len(lists1) + rate / len(lists2))/2, rate / len(lists1)

def work_for_E(papers, fid, typ):
	global all_total
	papers_more  = []
	f = open('jsons/'+fid+'-E.txt', "r")
	content = json.loads(f.read())
	for index, i in enumerate(content):
		if ('TITLE' in i):
			text = clear(i['TITLE'].lower().strip())
		else:
			print (index)
			text = clear(i['TITLE'].lower().strip())
		papers_more.append(text)
		content[index][typ] = False
	f.close()
	minzhong = 0.0
	left = 0.0
	print (papers)
	for j in papers:
		mx_rate = 0.0
		mx_index = None
		all_rate = 0.0
		all_index = None
		for index, k in enumerate(papers_more):
			tmp_rate, rate = check(j, k)
			if tmp_rate > mx_rate:
				mx_rate = tmp_rate
				mx_index = index
			if rate > all_rate:
				all_rate = rate
				all_index = index
		if mx_rate >= 0.8:
			content[mx_index][typ] = True
			minzhong += 1.0
		elif all_rate > 0.9:
			content[all_index][typ] = True
			minzhong += 1.0
		else:
			left+=1.0
			all_total[j] += 1.0
	print (name, left/(left+minzhong))
	logg.write("E:%f\n"%(left/(left+minzhong)))


def work_for_M(papers, fid, typ):
	global all_total
	papers_more  = []
	f = open('jsons/'+fid+'-M.txt', "r")
	content = json.loads(f.read())
	for index, i in enumerate(content):
		if 'title' in i:
			text = clear(i['title'].lower().strip())
		elif 'book title' in i:
			text = clear(i['book title'].lower().strip())
		elif 'original title' in i:
			text = clear(i['original title'].lower().strip())
		else:
			print (i)
			# text = clear(i['title'].lower().strip())
		papers_more.append(text)
		content[index][typ] = False
	f.close()
	minzhong = 0.0
	left = 0.0
	for j in papers:
		mx_rate = 0.0
		mx_index = None
		all_rate = 0.0
		all_index = None
		for index, k in enumerate(papers_more):
			tmp_rate, rate = check(j, k)
			if tmp_rate > mx_rate:
				mx_rate = tmp_rate
				mx_index = index
			if rate > all_rate:
				all_rate = rate
				all_index = index
		if mx_rate >= 0.8:
			content[mx_index][typ] = True
			minzhong += 1.0
		elif all_rate > 0.9:
			content[all_index][typ] = True
			minzhong += 1.0
		else:
			left+=1.0
			all_total[j] += 1.0
	print (name, left/(left+minzhong))
	logg.write("M:%f\n"%(left/(left+minzhong)))

logg = open("log.txt", "w")
files = os.listdir("./data/")
for name in files:
	name = "21-a"
	print (name)
	logg.write(name+"\n")
	if name == ".DS_Store":
		continue
	fid, typ = name.split("-")

	papers = []
	all_total = {}
	f = open('./data/' + name, "r")
	content = f.readlines()
	for i in content:
		res = (i.strip().strip('.').split('.'))
		if (len(res) > 1):
			papers.append(clear((".".join(res[1:-1])).strip().lower()))
			all_total[papers[-1]] = 0
	f.close()

	work_for_E(papers, fid, typ)
	work_for_M(papers, fid, typ)
	total = 0.0
	for i in all_total:
		if all_total[i] > 1.0:
			total += 1.0
	print (total / len(all_total))
	logg.write("total:%f\n"%(total / len(all_total)))
	logg.write("------------------\n")

logg.close()





