#!/usr/bin/python
import monkDebug as debug
import sys
import monkTools
import codeHL
import re


##
## @brief Transcode balise :
##   [code language=cpp]
##   int main(void) {
##   	return 0;
##   }
##   [/code]
## @param[in] value String to transform.
## @return Transformed string.
##
def transcode(value):
	#value = re.sub(r'\[code(( |\t|\n|\r)+style=(.*))?\](.*?)\[/code\]',
	"""
	value = re.sub(r'```(( |\t|\n|\r){\.(.*?))?\}(.*?)\```',
	               replace_code, #r'<pre>\4</pre>',
	               value,
	               flags=re.DOTALL)
	"""
	value = re.sub(r'```(( |\t|\n|\r)*(\{\.(.*?)\}))?(.*?)\```',
	               replace_code, #r'<pre>\4</pre>',
	               value,
	               flags=re.DOTALL)
	
	# TODO : remove the basic indentation of the element (to have a better display in the text tutorial ...
	return value

def transcode_part2(value):
	value = value.replace(":CODE:UNDER:SCORE:", "_")
	value = value.replace(":CODE:STAR:", "*")
	return value


def replace_code(match):
	if match.group() == "":
		return ""
	#debug.info("plop: " + str(match.groups()))
	#debug.info("code format: " + str(match.groups()[3]))
	value = codeHL.transcode(match.groups()[3], match.groups()[4])
	#value = value.replace("\n", "<br/>")
	value = value.replace("_", ":CODE:UNDER:SCORE:")
	value = value.replace("*", ":CODE:STAR:")
	return '<pre>' + str(value) + '</pre>'

