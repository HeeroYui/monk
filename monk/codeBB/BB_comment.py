#!/usr/bin/python
from realog import debug
import sys
from monk import tools
import re


##
## @brief Transcode balise:
##     /* ... */
## @param[in] value String to transform.
## @return Transformed string.
##
def transcode(value, _base_path):
	
	value = re.sub(r'\/\*(.*?)\*\/',
	               r'',
	               value,
	               flags=re.DOTALL)
	"""
	value = re.sub(r'\/\/(.*?)\n',
	               r'',
	               value)
	"""
	return value


