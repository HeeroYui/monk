#!/usr/bin/python
from realog import debug
import sys
from monk import tools
import re


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
	value = "\n" + value
	
	
	value = re.sub(r'@tableofcontents',
	               r'',
	               value)
	
	value = re.sub(r'\n(.*?)(( |\t)*\{.*\})*\n====*',
	               r'\n<h1>\1</h1>',
	               value)
	value = re.sub(r'\n(.*?)(( |\t)*\{.*\})*\n---*',
	               r'\n<h2>\1</h2>',
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
	
	value = value[1:]
	
	return value


