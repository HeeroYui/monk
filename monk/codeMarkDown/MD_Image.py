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
	value = re.sub(r'!\[(.*?)\][ \t]*\((.*?)\?w=([0-9]+)%\)',
	               r'<img src="' + base_path + r'\2" alt="\1" width="\3%"/>',
	               value)
	value = re.sub(r'!\[(.*?)\][ \t]*\((.*?)\?w=([0-9]+)px\)',
	               r'<img src="' + base_path + r'\2" alt="\1" width="\3px"/>',
	               value)
	value = re.sub(r'!\[(.*?)\][ \t]*\((.*?)\?h=([0-9]+)px\)',
	               r'<img src="' + base_path + r'\2" alt="\1" height="\3px"/>',
	               value)
	value = re.sub(r'!\[(.*?)\][ \t]*\((.*?)\?w=([0-9]+)px&h=([0-9]+)px\)',
	               r'<img src="' + base_path + r'\2" alt="\1" width="\3px" height="\4px"/>',
	               value)
	value = re.sub(r'!\[(.*?)\][ \t]*\((.*?)\)',
	               r'<img src="' + base_path + r'\2" alt="\1"/>',
	               value)
	return value


