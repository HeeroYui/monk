#!/usr/bin/python
from realog import debug
import sys
import monkTools
import re


##
## @brief Transcode 
## commencez les lignes par:
## *  
## *  
## 
## +  
## +  
## 
## resultat:
## 
##  	- 
##  	- 
##  	- 
## 
## commencez les lignes par:
## -  
## -  
## 
## resultat:
## 
##  	1. 
##  	2. 
##  	3. 
## 
## @param[in] value String to transform.
## @return Transformed string.
##
def transcode(value):
	value = re.sub(r'\n((  - )|(  * )|(  # ))',
	               r'\n:INDENT:[STAR]',
	               value)
	p = re.compile('((\:INDENT\:(.*?)\n)*)',
	               flags=re.DOTALL)
	value = p.sub(replace_wiki_identation,
	              value)
	value = re.sub(r'\[STAR\](.*?)\n',
	               r'<li>\1</li>',
	               value,
	               flags=re.DOTALL)
	return value


def replace_wiki_identation(match):
	if match.group() == "":
		return ""
	#debug.verbose("plop: " + str(match.group()))
	value  = "<ul>"
	value += re.sub(r':INDENT:',
	               r'',
	               match.group())
	value += "</ul>"
	return transcode(value)
