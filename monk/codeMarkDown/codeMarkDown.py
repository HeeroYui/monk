#!/usr/bin/python
from realog import debug
import sys
import monkTools
import re
"""
import BB_Link
import BB_Image
import BB_Table

import BB_Specification
"""
import MD_Text
import MD_IndentAndDot
import MD_Title
import MD_comment
import MD_lineReturn
import MD_Code
##
## @brief Transcode input data in the corect format.
## @param[in] string String to transform.
## @return Transformed string.
##
def transcode(value):
	# remove html property
	value = re.sub(r'&', r'&amp;', value)
	value = re.sub(r'<', r'&lt;', value)
	value = re.sub(r'>', r'&gt;', value)
	value = re.sub(r'\r\n', r'\n', value)
	value = re.sub(r'\n\r', r'\n', value)
	value = re.sub(r'\r', r'\n', value)
	value = MD_comment.transcode(value)
	value = MD_Title.transcode(value)
	value = MD_IndentAndDot.transcode(value)
	value = MD_Code.transcode(value)
	value = MD_lineReturn.transcode(value)
	value = MD_Text.transcode(value)
	"""
	value = BB_Text.transcode(value)
	value = BB_Link.transcode(value)
	value = BB_Image.transcode(value)
	value = BB_Table.transcode(value)
	value = BB_Specification.transcode(value)
	"""
	value = MD_Code.transcode_part2(value)
	return value

##
## @brief transcode a BBcode file in a html file
## @return True if the file is transformed
##
def transcode_file(inputFileName, outputFileName):
	inData = monkTools.file_read_data(inputFileName)
	if inData == "":
		return False
	outData = transcode(inData)
	debug.warning(" out: " + outputFileName)
	monkTools.file_write_data(outputFileName, outData)
	return True


