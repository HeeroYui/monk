#!/usr/bin/python
from realog import debug
import sys
from monk import tools
import re
import os

image_base_path = ""

def simplify_path(aaa):
	#debug.warning("ploppppp " + str(aaa))
	st = []
	aaa = aaa.split("/")
	for i in aaa:
		if i == '..':
			if len(st) > 0:
				st.pop()
			else:
				continue
		elif i == '.':
			continue
		elif i != '':
			if len(st) > 0:
				st.append("/" + str(i))
			else:
				st.append(str(i))
	if len(st) == 1:
		return "/"
	#debug.error("ploppppp " + str(st))
	return "".join(st)


##
## @brief Transcode balise:
##     [img w=125 h=45]dossier/image.jpg[/img]
##     [img w=125 h=45]http://plop.com/dossier/image.png[/img]
## @param[in] value String to transform.
## @return Transformed string.
##
def transcode(value, _base_path):
	global image_base_path
	if len(_base_path) != 0:
		base_path = (_base_path + '/').replace('/',':IMAGE:UNDER:SCORE::IMAGE:UNDER:SCORE:')
		image_base_path = _base_path
	else:
		image_base_path = ""
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
	#value = re.sub(r':BASE_PATH:',
	#               r'' + base_path,
	#               value)
	return value


def transcode_part2(value):
	value = value.replace(":IMAGE:UNDER:SCORE:", "_")
	value = value.replace(":IMAGE:STAR:", "*")
	value = value.replace(":IMAGE:BRACKET:START:", "[")
	value = value.replace(":IMAGE:BRACKET:STOP:", "]")
	value = value.replace(":IMAGE:SLASH:", "/")
	return value

def replace_image(match):
	global image_base_path
	if match.group() == "":
		return ""
	debug.verbose("Image parse: " + str(match.group()))
	#value  = '<img src=":BASE_PATH:'
	value  = '<img src="'
	value += simplify_path(os.path.join(image_base_path, match.groups()[1])).replace("/", "__")
	value += '" '
	
	alt_properties = match.groups()[0].split("|")
	alt = False
	center = False
	right = False
	left = False
	showTitle = False
	title = False
	type = "Image"
	for elem in alt_properties:
		if alt == False:
			alt = True
			value += 'alt="' + elem + '" '
			title = elem
			continue
		key_alt, value_alt = elem.split("=")
		if key_alt == "width":
			value += 'width="' + value_alt + '" '
		elif key_alt == "height":
			value += 'height="' + value_alt + '" '
		if key_alt == "align":
			if value_alt == "center":
				center = True
			if value_alt == "right":
				right = True
			if value_alt == "left":
				left = True
		if key_alt == "type":
			type = value_alt
		if key_alt == "titleShow":
			if elem == "false":
				showTitle = False
			else:
				showTitle = True
		else:
			debug.warning("not manage element '" + key_alt + "' in '" + str(match.group()) + "'")
	value += '/>'
	value = value.replace("_", ":IMAGE:UNDER:SCORE:")
	value = value.replace("*", ":IMAGE:STAR:")
	value = value.replace("[", ":IMAGE:BRACKET:START:")
	value = value.replace("]", ":IMAGE:BRACKET:STOP:")
	value = value.replace(":BASE:IMAGE:UNDER:SCORE:PATH:", ":BASE_PATH:")
	
	if showTitle == True:
		value = "<br/>" + value + "<br/><u><b>Image: </b>" + title + "</u><br/>"
	
	if center == True:
		value = "<center>" + value + "</center>"
	elif right == True:
		value = "<right>" + value + "</right>"
	elif left == True:
		value = "<left>" + value + "</left>"
	
	return value


