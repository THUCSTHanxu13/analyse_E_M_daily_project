import os
import re

def check(str):
	for i in str:
		if i == " " or i.isalpha():
			continue
		else:
			return False
	return True

hash_M = {}
tags_M = []

hash_E = {}
tags_E = []

def work_M(file_name):
	print (file_name)
	print ("=========")
	lastsection = False
	f = open('./results/' + file_name, 'r')
	for i in f.readlines():
		if lastsection:
			if i.strip() == "Publication Type":
				lastsection = False
			else:
				continue
		if i.lstrip() != i:
			continue
		i = i.strip()
		if i.split()[0] == 'VI':
			continue
		if check(i):
			if not i in hash_M:
				hash_M[i] = 1
				tags_M.append(i)
				print (i)
			else:
				hash_M[i] += 1
		if i == "Section":
			lastsection = True
	f.close()

def work_E(file_name):
	print (file_name)
	print ("=========")
	lastsection = False
	f = open('./results/' + file_name, 'r')
	for i in f.readlines():
		if i.lstrip() != i:
			continue
		i = i.strip()
		if check(i) and i.upper() == i:
			if not i in hash_E:
				hash_E[i] = 1
				tags_E.append(i)
				print (i)
			else:
				hash_E[i] += 1
	f.close()


file_list = os.listdir("./results/")
for file_name in file_list:
	# if file_name.find("M") != -1:
	# 	work_M(file_name.strip())
	# 	print (len(tags_M))
	# 	break
	if file_name.find("E") != -1:
		work_E(file_name.strip())
		# break

for i in tags_E:
	print (i,"\t",hash_E[i])