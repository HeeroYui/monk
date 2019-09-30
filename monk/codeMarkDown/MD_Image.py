#!/usr/bin/python
from realog import debug
import sys
from monk import tools
import re


##
## @brief Transcode balise:
##     [img w=125 h=45]dossier/image.jpg[/img]
##     [img w=125 h=45]http://plop.com/dossier/image.png[/img]
## @param[in] value String to transform.
## @return Transformed string.
##
def transcode(value, _base_path):
	if len(_base_path) != 0:
		base_path = (_base_path + '/').replace('/','__')
	else:
		base_path = ""
	# named image : ![hover Value](http://sdfsdf.svg)
	value = re.sub(r'!\[http://(.*?)\][ \t]*\((.*?)\)',
	               r'<img src="http://\2" alt="\1"/>',
	               value)
	value = re.sub(r'!\[https://(.*?)\][ \t]*\((.*?)\)',
	               r'<img src="https://\2" alt="\1"/>',
	               value)
	
	p = re.compile('!\[(.*?)\][ \t]*\((.*?)\)')
	value = p.sub(replace_image,
	              value)
	value = re.sub(r':BASE_PATH:',
	               r'' + base_path,
	               value)
	return value



def replace_image(match):
	if match.group() == "":
		return ""
	debug.verbose("Image parse: " + str(match.group()))
	value  = '<img src=":BASE_PATH:'
	value += match.groups()[1].replace("/", "__")
	value += '" '
	
	alt_properties = match.groups()[0].split("|")
	alt = False
	for elem in alt_properties:
		if alt == False:
			alt = True
			value += 'alt="' + elem + '" '
			continue
		key_alt, value_alt = elem.split("=")
		if key_alt == "width":
			value += 'width="' + value_alt + '" '
		elif key_alt == "height":
			value += 'height="' + value_alt + '" '
		else:
			debug.warning("not manage element '" + key_alt + "' in '" + str(match.group()) + "'")
	value += '/>'
	return value
