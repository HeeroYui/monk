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
##      +-------------------------------------+
##      | colone 1                            |
##      +------------------+------------------+
##      | ligne 1          | colone 2 ligne 1 |
##      +------------------+------------------+
##      | colone 1 ligne 1 | colone 2 ligne 2 |
##      +------------------+------------------+
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



def replace_table(match):
	if match.group() == "":
		return ""
	#debug.verbose("plop: " + str(match.group()))
	value  = "<table>"
	p = re.compile('\n(.*)')
	value += p.sub(replace_table_line,
	              match.group())
	value += "</table>"
	return value

def replace_table_line(match):
	if match.group() == "":
		return ""
	debug.warning("parse LINE ... : '" + str(match.group()) + "'")
	value  = "<tr>"
	tmpppp = match.group().replace("\n", "").split('|')
	for elem in tmpppp:
		if len(elem) == 0:
			continue
		value += "<td>" + elem + "</td>"
	value += "</tr>"
	debug.warning("    ==> out " + value)
	return value
