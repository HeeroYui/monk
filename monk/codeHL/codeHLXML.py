#!/usr/bin/python
from realog import debug
import sys
from monk import tools
import re

listRegExp = [
	[ r'&lt;!\-\-!(.*?)\-\-&gt;', 'code-doxygen'],
	[ r'&lt;!\-\-(.*?)\-\-&gt;', 'code-comment'],
	[ r'"((\\"|.)*?)"', 'code-text-quote'],
	[ r"'(('|.)*?)'", 'code-text-quote'],
	[ r'&lt;/[0-9a-zA-Z_]+|&lt;[0-9a-zA-Z_]+|/&gt;|&gt;',
	  'code-function-name']
]

def transcode(value):
	inValue = value
	outValue = ""
	haveFindSomething = False;
	for reg1, color in listRegExp:
		result = re.search(reg1, inValue, re.DOTALL)
		while result != None:
			haveFindSomething = True
			# sub parse the start : 
			outValue += transcode(inValue[:result.start()])
			# transform local
			outValue += '<span class="' + color + '">'
			outValue += result.group()
			outValue += '</span>'
			
			# change the input value
			inValue = inValue[result.end():]
			# Search again ...
			result = re.search(reg1, inValue, re.DOTALL)
	outValue += inValue
	return outValue
