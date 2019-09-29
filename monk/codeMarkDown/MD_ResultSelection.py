#!/usr/bin/python
from realog import debug
import sys
from monk import tools
import re


##
## @brief Transcode 
## commencez les lignes par:
##
def transcode(value, _base_path = ""):
	p = re.compile('\[([a-zA-Z0-9_-\| ]*)\]',
	               flags=re.DOTALL)
	value = p.sub(replace_result_list,
	              value)
	return value


def replace_result_list(match):
	if match.group() == "":
		return ""
	debug.warning("parse RESULT ... : '" + str(match.group()) + "'")
	value  = '<table id="my-table"><tr>'
	tmpppp = match.group().replace("]", "").replace("[", "").replace("\n", "").split('|')
	for elem in tmpppp:
		if len(elem) == 0:
			continue
		value += '<td>' + elem + "</td>"
	value += "</tr></table>"
	debug.warning("    ==> out " + value)
	return value
