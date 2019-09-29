#!/usr/bin/python
from realog import debug
import sys
from monk import tools
import re

listRegExp = [
	[ r'"((\\"|.)*?)"', 'code-text-quote'],
	[ r"'(('|.)*?)'", 'code-text-quote'],
	[ r'(true|false|null)',
	  'code-type'],
	[ r'(((0(x|X)[0-9a-fA-F]*)|(\d+\.?\d*|\.\d+)((e|E)(\+|\-)?\d+)?)(L|l|UL|ul|u|U|F|f)?)',
	  'code-type']
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

