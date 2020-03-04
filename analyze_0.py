#coding:utf-8
import os
import BeautifulSoup
import re
import json

def work(section):

	title = section.find("h3", {'class':'title'})
	title = title.string.lower().strip()

	if title.find("included") != -1:
		typ = 'in'
		style = {'class':"bibliographies references_includedStudies"}
	elif title.find("excluded") != -1:
		typ = 'ex'
		style = {'class':"bibliographies references_excludedStudies"}
	elif title.find("awaiting") != -1:
		typ = 'a'
		style = {'class':"bibliographies references_awaitingAssessmentStudies"}
	elif title.find("ongoing") != -1:
		typ = 'a'
		style = {'class':"bibliographies references_ongoingStudies"}
	elif title.find("additional") != -1:
		typ = 'a'
		style = {'class':"bibliographies references_additionalReferences"}
	else:
		return [], None

	res = []

	articles = section.findAll('div', style)
	for i in articles:
		try:
		
			title = i.find('span', {'class':'citation-title'})
			if title == None:
				title = i.find('span', {'class':'citation'})
				print ("hx")
			title = title.string.strip()

			year = i.find('span', {'class':'pubYear'})
			if year == None:
				context = i.text
				year = re.search('20\d\d', context)
				if year == None:
					year = re.search('19\d\d', context).group(0)
				else:
					year = year.group(0)
			else:
				year = year.string.strip()

			res.append((title, year))

		except Exception, err:
			print ("ggg")

	return res, typ

data_lists = os.listdir('./web/')
res_lists = os.listdir('./new/')

for nam in data_lists:
	uid = nam.replace(".html", ".json")
	if uid in res_lists:
		continue

	f = open("./web/"+nam, "r")
	content = f.read()
	f.close()

	html = BeautifulSoup.BeautifulSoup(content)

	articles = {}

	sections = html.findAll('section')
	for section in sections:
		if section.find('div', {'class':'section-header'}) != None:
			res, typ = work(section)
			if typ != None:
				if not typ in articles:
					articles[typ] = []
				articles[typ] = articles[typ] + res

	
	for i in articles:
		print (i, len(articles[i]))
	f = open("./new/"+uid, "w")
	f.write(json.dumps(articles))
	f.close()

