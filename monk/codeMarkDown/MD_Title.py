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
	
	
	value = re.sub(r'@tableofcontents',
	               r'',
	               value)
	
	value = re.sub(value_start + r'(.*?)(( |\t)*\{.*\})*\n====*',
	               value_start + r'<h1>\1</h1>',
	               value)
	value = re.sub(r'\n(.*?)(( |\t)*\{.*\})*\n===*',
	               r'\n<h2>\1</h2>',
	               value)
	value = re.sub(r'\n(.*?)(( |\t)*\{.*\})*\n---*',
	               r'\n<h3>\1</h3>',
	               value)
	value = re.sub(r'\n(.*?)(( |\t)*\{.*\})*\n\+\+\+*',
	               r'\n<h4>\1</h4>',
	               value)
	value = re.sub(r'\n(.*?)(( |\t)*\{.*\})*\n~~~*',
	               r'\n<h5>\1</h5>',
	               value)
	
	value = re.sub(r'\n###### (.*?)(( |\t)*\{.*\})* ######',
	               r'\n<h6>\1</h6>',
	               value)
	value = re.sub(r'\n###### (.*?)(( |\t)*\{.*\})*',
	               r'\n<h6>\1</h6>',
	               value)
	
	value = re.sub(r'\n##### (.*?)(( |\t)*\{.*\})* #####',
	               r'\n<h5>\1</h5>',
	               value)
	value = re.sub(r'\n##### (.*?)(( |\t)*\{.*\})*',
	               r'\n<h5>\1</h5>',
	               value)
	
	value = re.sub(r'\n#### (.*?)(( |\t)*\{.*\})* ####',
	               r'\n<h4>\1</h4>',
	               value)
	value = re.sub(r'\n#### (.*?)(( |\t)*\{.*\})*',
	               r'\n<h4>\1</h4>',
	               value)
	
	value = re.sub(r'\n### (.*?)(( |\t)*\{.*\})* ###',
	               r'\n<h3>\1</h3>',
	               value)
	value = re.sub(r'\n### (.*?)(( |\t)*\{.*\})*',
	               r'\n<h3>\1</h3>',
	               value)
	
	value = re.sub(r'\n## (.*?)(( |\t)*\{.*\})* ##',
	               r'\n<h2>\1</h2>',
	               value)
	value = re.sub(r'\n## (.*?)(( |\t)*\{.*\})*',
	               r'\n<h2>\1</h2>',
	               value)
	
	value = re.sub(value_start,
	               r'',
	               value)
	
	return value



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