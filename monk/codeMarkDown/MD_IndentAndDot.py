#!/usr/bin/python
from realog import debug
import sys
from monk import tools
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
def transcode(value, _base_path = ""):
	value = re.sub(r'\n((  - \[ \] )|(  \* \[ \] )|(  # \[ \] )|(\* \[ \] ))',
	               r'\n:INDENT_1:[CHECK_BOX_0]',
	               value)
	value = re.sub(r'\n((  - \[x\] )|(  \* \[x\] )|(  # \[x\] )|(\* \[x\] ))',
	               r'\n:INDENT_1:[CHECK_BOX_1]',
	               value)
	value = re.sub(r'\n((  - \[X\] )|(  \* \[X\] )|(  # \[X\] )|(\* \[X\] ))',
	               r'\n:INDENT_1:[CHECK_BOX_2]',
	               value)
	value = re.sub(r'\n((  - )|(  \* )|(  # )|(\*  ))',
	               r'\n:INDENT_1:[TICK]',
	               value)
	value = re.sub(r'\n((  - )|(  \* )|(  # )|(\*  ))',
	               r'\n:INDENT_1:[STAR]',
	               value)
	value = re.sub(r'\n((  - )|(  \* )|(  # )|(\*  ))',
	               r'\n:INDENT_1:[SHARP]',
	               value)
	value = re.sub(r'\n((  - )|(  \* )|(  # )|(\*  ))',
	               r'\n:INDENT_1:[STAR]',
	               value)
	value = re.sub(r'\n(    |\t)((  - \[ \] )|(  \* \[ \] )|(  # \[ \] )|(\* \[ \] ))',
	               r'\n:INDENT_1::INDENT_2:[CHECK_BOX_0]',
	               value)
	value = re.sub(r'\n(    |\t)((  - \[x\] )|(  \* \[x\] )|(  # \[x\] )|(\* \[x\] ))',
	               r'\n:INDENT_1::INDENT_2:[CHECK_BOX_1]',
	               value)
	value = re.sub(r'\n(    |\t)((  - \[X\] )|(  \* \[X\] )|(  # \[x\] )|(\* \[x\] ))',
	               r'\n:INDENT_1::INDENT_2:[CHECK_BOX_2]',
	               value)
	value = re.sub(r'\n(    |\t)((  - )|(  \* )|(  # )|(\*  ))',
	               r'\n:INDENT_1::INDENT_2:[STAR]',
	               value)
	value = re.sub(r'\n(        |\t\t)((  - \[ \] )|(  \* \[ \] )|(  # \[ \] )|(\* \[ \] ))',
	               r'\n:INDENT_1::INDENT_2::INDENT_3:[CHECK_BOX_0]',
	               value)
	value = re.sub(r'\n(        |\t\t)((  - \[x\] )|(  \* \[x\] )|(  # \[x\] )|(\* \[x\] ))',
	               r'\n:INDENT_1::INDENT_2::INDENT_3:[CHECK_BOX_1]',
	               value)
	value = re.sub(r'\n(        |\t\t)((  - \[X\] )|(  \* \[X\] )|(  # \[X\] )|(\* \[X\] ))',
	               r'\n:INDENT_1::INDENT_2::INDENT_3:[CHECK_BOX_2]',
	               value)
	value = re.sub(r'\n(        |\t\t)((  - )|(  \* )|(  # )|(\*  ))',
	               r'\n:INDENT_1::INDENT_2::INDENT_3:[STAR]',
	               value)
	p = re.compile('((\:INDENT_1\:(.*?)\n)*)',
	               flags=re.DOTALL)
	value = p.sub(replace_wiki_identation_1,
	              value)
	
	value = re.sub(r'\[STAR\](.*?)\n',
	               r'<li class="list-star">\1</li>',
	               value,
	               flags=re.DOTALL)
	value = re.sub(r'\[SHARP\](.*?)\n',
	               r'<li class="list-sharp">\1</li>',
	               value,
	               flags=re.DOTALL)
	value = re.sub(r'\[TICK\](.*?)\n',
	               r'<li class="list-tick">\1</li>',
	               value,
	               flags=re.DOTALL)
	value = re.sub(r'\[NUMBER\](.*?)\n',
	               r'<li class="list-number">\1</li>',
	               value,
	               flags=re.DOTALL)
	value = re.sub(r'\[CHECK_BOX_2\](.*?)\n',
	               #r'<li class="list-check-box"><input type="checkbox" checked=""/>\1</li>',
	               r'<li class="list-check-box-tick">\1</li>',
	               value,
	               flags=re.DOTALL)
	value = re.sub(r'\[CHECK_BOX_1\](.*?)\n',
	               #r'<li class="list-check-box"><input type="checkbox" checked=""/>\1</li>',
	               r'<li class="list-check-box-check">\1</li>',
	               value,
	               flags=re.DOTALL)
	value = re.sub(r'\[CHECK_BOX_0\](.*?)\n',
	               #r'<li class="list-check-box"><input type="checkbox"/>\1</li>',
	               r'<li class="list-check-box">\1</li>',
	               value,
	               flags=re.DOTALL)
	
	
	return value


def replace_wiki_identation_1(match):
	if match.group() == "":
		return ""
	#debug.verbose("plop: " + str(match.group()))
	value  = "<ul>\n"
	value += re.sub(r':INDENT_1:',
	               r'',
	               match.group())
	value += "\n</ul>"
	
	p = re.compile('((\:INDENT_2\:(.*?)\n)*)',
	               flags=re.DOTALL)
	value = p.sub(replace_wiki_identation_2,
	              value)
	
	return value

def replace_wiki_identation_2(match):
	if match.group() == "":
		return ""
	#debug.verbose("plop: " + str(match.group()))
	value  = "<ul>\n"
	value += re.sub(r':INDENT_2:',
	               r'',
	               match.group())
	value += "\n</ul>"
	
	p = re.compile('((\:INDENT_3\:(.*?)\n)*)',
	               flags=re.DOTALL)
	value = p.sub(replace_wiki_identation_3,
	              value)
	
	return value

def replace_wiki_identation_3(match):
	if match.group() == "":
		return ""
	#debug.verbose("plop: " + str(match.group()))
	value  = "<ul>\n"
	value += re.sub(r':INDENT_3:',
	               r'',
	               match.group())
	value += "\n</ul>"
	return value


