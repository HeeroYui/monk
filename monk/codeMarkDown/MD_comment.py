#!/usr/bin/python
from realog import debug
import sys
import monkTools
import re

_comment_code = "[comment]:"
##
## @brief Transcode balise:
##     line start with [comment]:
## @param[in] value String to transform.
## @return Transformed string.
##
def transcode(value):
	out = "";
	for elem in value.split("\n"):
		if     len(elem) >= len(_comment_code) \
		   and elem[:len(_comment_code)] == _comment_code:
			continue
		out += elem + "\n"
	return out


