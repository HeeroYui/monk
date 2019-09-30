#!/usr/bin/python
from realog import debug
import sys
from monk import tools
import re
import os

basic_link_path = ""

##
## @brief Transcode:
## [http://votre_site.con] => http://votre_site.con
## [http://votre_site.con | text displayed] => text displayed
## [http://votre_site.con text displayed] => text displayed.
## 
## @param[in] value String to transform.
## @return Transformed string.
##
def transcode(value, _base_path):
	global basic_link_path
	basic_link_path = _base_path
	if len(_base_path) != 0:
		base_path = (_base_path + '/').replace('/','__')
	else:
		base_path = ""
	# named image : ![hover Value](http://sdfsdf.svg)
	value = re.sub(r'\[(.*?)\][ \t]*\(http://(.*?)\)',
	               r'<a href="http://\2">\1</a>',
	               value)
	value = re.sub(r'\[(.*?)\][ \t]*\(https://(.*?)\)',
	               r'<a href="https://\2">\1</a>',
	               value)
	"""
	value = re.sub(r'\[(.*?)\][ \t]*\((.*?)\.md\)',
	               r'<a href="' + base_path + r'\2.html">\1</a>',
	               value)
	"""
	p = re.compile('\[(.*?)\][ \t]*\((.*?)\.md\)')
	value = p.sub(replace_link,
	              value)
	p = re.compile('\[(.*?)\][ \t]*\((.*?)\)')
	value = p.sub(replace_link,
	              value)
	
	return value


def replace_link(match):
	global basic_link_path
	if match.group() == "":
		return ""
	debug.warning("plop: " + str(match.group()))
	debug.warning("plop: " + str(match.groups()))
	value  = '<a href="'
	if basic_link_path != "":
		link = os.path.join(basic_link_path, match.groups()[1]);
		debug.warning("BASIC path : " + link)
		link = os.path.normpath(link)
		debug.warning("        ==>  " + link)
	else:
		link = match.groups()[1]
	
	value += link.replace("/", "__")
	if match.groups()[0] != "":
		value += '.html">' + match.groups()[0] + '</a>'
	else:
		value += '.html">' + match.groups()[1] + '</a>'
	return value

