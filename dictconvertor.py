# _*_ coding: utf-8 _*_

import csv, codecs, json

Dict={}
with codecs.open('Dict/TOEFLdictraw.txt', 'r') as f:
	for line in f:
		(lkey, lword, lpart, lvalue) = line.strip().split()
		Dict[lword]=[lpart+' '+lvalue]
		if lkey=='1': break
	for line in f:
		(key, word, part, value) = line.strip().split('\t')
		if word==' ':
			Dict[lword].append(part+' '+value)
		else:
			Dict[word]=[part+' '+value]
			(lkey, lword, lpart, lvalue)=(key, word, part, value)
			
	

json.dump(Dict, open("Dict/TOEFLdict.dat",'w'))

mydict = json.load(open("Dict/TOEFLdict.dat"))

for word in mydict.keys():
	print word, mydict[word][0]

for interp in mydict['yield']:
	print interp