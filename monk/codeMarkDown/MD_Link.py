#!/usr/bin/python
from realog import debug
import sys
from monk import tools
import re


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
	
	"""
	# named link : [[http://plop.html | link name]]
	value = re.sub(r'\[\[http://(.*?) \| (.*?)\]\]',
	               r'<a href="http://\1">\2</a>',
	               value)
	
	# direct link : [[http://plop.html]]
	value = re.sub(r'\[\[http://(.*?)\]\]',
	               r'<a href="http://\1">http://\1</a>',
	               value)
	# named link : [[https://plop.html | link name]]
	value = re.sub(r'\[\[https://(.*?) \| (.*?)\]\]',
	               r'<a href="https://\1">\2</a>',
	               value)
	
	# direct link : [[https://plop.html]]
	value = re.sub(r'\[\[https://(.*?)\]\]',
	               r'<a href="https://\1">http://\1</a>',
	               value)
	
	# direct lib link : [lib[libname]]
	value = re.sub(r'\[lib\[(.*?) \| (.*?)\]\]',
	               r'<a href="../\1">\2</a>',
	               value)
	
	value = re.sub(r'\[doc\[(.*?) \| (.*?)\]\]',
	               r'<a href="\1.html">\2</a>',
	               value)
	
	value = re.sub(r'\[tutorial\[(.*?) \| (.*?)\]\]',
	               r'<a href="tutorial_\1.html">\2</a>',
	               value)
	
	value = re.sub(r'\[(lib|class|methode)\[(.*?)\]\]',
	               replace_link_class,
	               value)
	"""
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
	if match.group() == "":
		return ""
	debug.verbose("plop: " + str(match.group()))
	value  = '<a href="'
	value += match.groups()[1].replace("/", "__")
	value += '.html">' + match.groups()[0] + '</a>'
	return value


def replace_link_class(match):
	if match.group() == "":
		return ""
	#debug.info("plop: " + str(match.group()))
	if match.groups()[0] == 'class':
		className = match.groups()[1]
		value = re.sub(':', '_', className)
		return '<a href="class_' + value + '.html">' + className + '</a>'
	elif match.groups()[0] == 'lib':
		return match.groups()[1]
	elif match.groups()[0] == 'methode':
		return match.groups()[1]
	else:
		return match.groups()[1]



