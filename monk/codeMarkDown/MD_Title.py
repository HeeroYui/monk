#!/usr/bin/python
from realog import debug
import sys
from monk import tools
import re

h2counter = 1
h3counter = 1
h4counter = 1
h5counter = 1
h6counter = 1
indexation = ""

##
## @brief Transcode .
##      =?=Page Title=?=
##      ==Title 1==
##      ===Title 2===
##      ====Title 3====
##      =====Title 4=====
##      ======Title 5======
## @param[in] value String to transform.
## @return Transformed string.
##
def transcode(value, _base_path):
	value_start = "==Z==!!START!!==Z=="
	value = value_start + value
	global h2counter
	global h3counter
	global h4counter
	global h5counter
	global h6counter
	global indexation
	h2counter = 1
	h3counter = 1
	h4counter = 1
	h5counter = 1
	h6counter = 1
	indexation = ""
	
	value = re.sub(r'@tableofcontents',
	               r'',
	               value)
	
	value = re.sub(value_start + r'(.*?)(( |\t)*\{.*\})*\n====*',
	               value_start + r'<h1>\1</h1>',
	               value)
	value = re.sub(r'\n(.*?)(( |\t)*\{.*\})*\n===*',
	               r'\n==Z==222==Z==\1</h2>',
	               value)
	value = re.sub(r'\n(.*?)(( |\t)*\{.*\})*\n---*',
	               r'\n==Z==333==Z==\1</h3>',
	               value)
	value = re.sub(r'\n(.*?)(( |\t)*\{.*\})*\n\+\+\+*',
	               r'\n==Z==444==Z==\1</h4>',
	               value)
	value = re.sub(r'\n(.*?)(( |\t)*\{.*\})*\n~~~*',
	               r'\n==Z==555==Z==\1</h5>',
	               value)
	
	"""
	value = re.sub(r'\n###### (.*?)(( |\t)*\{.*\})* ######',
	               r'\n==Z==666==Z==\1</h6>',
	               value)
	value = re.sub(r'\n###### (.*?)(( |\t)*\{.*\})*',
	               r'\n==Z==666==Z==\1</h6>',
	               value)
	"""
	
	value = re.sub(r'\n##### (.*?)(( |\t)*\{.*\})* #####',
	               r'\n==Z==666==Z==\1</h5>',
	               value)
	value = re.sub(r'\n##### (.*?)(( |\t)*\{.*\})*\n',
	               r'\n==Z==666==Z==\1</h5>\n',
	               value)
	
	value = re.sub(r'\n#### (.*?)(( |\t)*\{.*\})* ####',
	               r'\n==Z==555==Z==\1</h4>',
	               value)
	value = re.sub(r'\n#### (.*?)(( |\t)*\{.*\})*\n',
	               r'\n==Z==555==Z==\1</h4>\n',
	               value)
	
	value = re.sub(r'\n### (.*?)(( |\t)*\{.*\})* ###',
	               r'\n==Z==444==Z==\1</h3>',
	               value)
	value = re.sub(r'\n### (.*)(( |\t)*\{.*\})*\n',
	               r'\n==Z==444==Z==\1</h3>\n',
	               value)
	
	value = re.sub(r'\n## (.*?)(( |\t)*\{.*\})* ##',
	               r'\n==Z==333==Z==\1</h2>',
	               value)
	value = re.sub(r'\n## (.*?)(( |\t)*\{.*\})*\n',
	               r'\n==Z==333==Z==\1</h2>\n',
	               value)
	
	value = re.sub(r'\n# (.*?)(( |\t)*\{.*\})* #',
	               r'\n==Z==333==Z==\1</h2>',
	               value)
	value = re.sub(r'\n# (.*?)(( |\t)*\{.*\})*\n',
	               r'\n==Z==333==Z==\1</h2>\n',
	               value)
	
	value = re.sub(value_start,
	               r'',
	               value)
	
	p = re.compile('==Z==(222|333|444|555|666)==Z==')
	value = p.sub(replace_index_title,
	               value)
	return value


def replace_index_title(match):
	global h2counter
	global h3counter
	global h4counter
	global h5counter
	global h6counter
	global indexation
	if match.groups()[0] == "222":
		out = "<h2>" + str(h2counter) + ". "
		#indexation += "<h2>" + h2counter + ". "
		h2counter += 1
		h3counter = 1
		h4counter = 1
		h5counter = 1
		h6counter = 1
		return out
	if match.groups()[0] == "333":
		out = "<h3>" + str(h2counter) + "." + str(h3counter) + ". "
		h3counter += 1
		h4counter = 1
		h5counter = 1
		h6counter = 1
		return out
	if match.groups()[0] == "444":
		out = "<h4>" + str(h2counter) + "." + str(h3counter) + "." + str(h4counter) + ". "
		h4counter += 1
		h5counter = 1
		h6counter = 1
		return out
	if match.groups()[0] == "555":
		out = "<h5>" + str(h2counter) + "." + str(h3counter) + "." + str(h4counter) + "." + str(h5counter) + ". "
		h5counter += 1
		h6counter = 1
		return out
	if match.groups()[0] == "666":
		out = "<h6>" + str(h2counter) + "." + str(h3counter) + "." + str(h4counter) + "." + str(h5counter) + "." + str(h6counter) + ". "
		h6counter += 1
		return out
	return match.group()


def transcode_clean_empty_line_after(value, _base_path):
	value = re.sub(r'</h6>[\n \t]*<br/>',
	               r'</h6>',
	               value)
	value = re.sub(r'</h5>[\n \t]*<br/>',
	               r'</h5>',
	               value)
	value = re.sub(r'</h4>[\n \t]*<br/>',
	               r'</h4>',
	               value)
	value = re.sub(r'</h3>[\n \t]*<br/>',
	               r'</h3>',
	               value)
	value = re.sub(r'</h2>[\n \t]*<br/>',
	               r'</h2>',
	               value)
	value = re.sub(r'</h1>[\n \t]*<br/>',
	               r'</h1>',
	               value)
	return value