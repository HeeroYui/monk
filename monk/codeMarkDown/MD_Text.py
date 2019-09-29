#!/usr/bin/python
from realog import debug
import sys
from monk import tools
import re


##
## @brief Transcode .
##      [b]texte ici[/b]
##      [i]texte ici[/i]
##      [u]texte ici[/u]
##      [strike]texte ici[/strike]
##      [color=olive]texte ici[/color]
##      [color=#456FF33F]texte ici[/color]
##      Left : [left]texte ici[/left]
##      Center : [center]texte ici[/center]
##      Right : [right]texte ici[/right]
##      [size=22]sdfgsdfgsdgsfd[/size]
##      [cadre]mettre les code ici[/cadre]
## @param[in] string String to transform.
## @return Transformed string.
##
def transcode(value, _base_path):
	
	value = re.sub(r'\*\*(.*?)\*\*',
	               r'<strong>\1</strong>',
	               value,
	               flags=re.DOTALL)
	value = re.sub(r'__(.*?)__',
	               r'<strong>\1</strong>',
	               value,
	               flags=re.DOTALL)
	               
	value = re.sub(r'\*(.*?)\*',
	               r'<em>\1</em>',
	               value,
	               flags=re.DOTALL)
	"""
	value = re.sub(r'_(.*?)_',
	               r'<em>\1</em>',
	               value,
	               flags=re.DOTALL)
	"""
	value = re.sub(r'____(.*?)\n',
	               r'<hr>',
	               value,
	               flags=re.DOTALL)
	
	return value
