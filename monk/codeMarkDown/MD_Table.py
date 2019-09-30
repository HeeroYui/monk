#!/usr/bin/python
from realog import debug
import sys
from monk import tools
import re


##
## @brief Transcode table:
##      | colone 1 ||
##      | ligne 1 |	colone 2 ligne 1 |
##      | colone 1 ligne 1 | colone 2 ligne 2|
## Avec autant de ligne et de colone que vous voullez..
## Il est possible de faire des retour a la ligne dans une case du tableau...
## En bref sa tend a marcher comme sur un Wiki...
## 
## result:
##      | colone 1         |                  |
##      | ---------------- | ---------------- |
##      | ligne 1          | colone 2 ligne 1 |
##      | colone 1 ligne 1 | colone 2 ligne 2 |
## 
## @param[in] value String to transform.
## @return Transformed string.
##
def transcode(value, _base_path):
	
	p = re.compile('((\n\|(.*)\|)*)',
	              flags=re.DOTALL)
	value = p.sub(replace_table,
	              value)
	return value

table_index = 0

def replace_table(match):
	global table_index
	table_index = 0
	if match.group() == "":
		return ""
	debug.warning("=============================: " + str(match.group()))
	value = '<table class="doc_table">'
	value_global = re.sub(r'\n\|([\t -]*\|)+',
	                      r'',
	                      match.group())
	#value_global = match.group()
	debug.warning("=============================: " + str(value_global))
	p = re.compile('\n(.*)')
	value += p.sub(replace_table_line,
	               value_global)
	value += "</table>"
	return value

def replace_table_line(match):
	global table_index
	if match.group() == "":
		return ""
	debug.warning("parse LINE ... : '" + str(match.group()) + "' ==> " + str(table_index))
	value  = "<tr>"
	tmpppp = match.group().replace("\n", "").split('|')
	for elem in tmpppp:
		if len(elem) == 0:
			continue
		if table_index == 0:
			value += "<th>" + elem + "</th>"
		else:
			value += "<td>" + elem + "</td>"
	value += "</tr>"
	table_index += 1
	debug.warning("    ==> out " + value)
	return value
