#!/usr/bin/python
from realog import debug
import sys
from monk import tools
import re
import BB_Title
import BB_Text
import BB_IndentAndDot
import BB_Link
import BB_Image
import BB_Table

import BB_comment
import BB_lineReturn
import BB_Code
import BB_Specification

##
## @brief Transcode input data in the corect format.
## @param[in] string String to transform.
## @return Transformed string.
##
def transcode(value, _base_path = ""):
	# remove html property
	value = re.sub(r'<', r'&lt;', value)
	value = re.sub(r'>', r'&gt;', value)
	value = BB_comment.transcode(value, _base_path)
	value = BB_Title.transcode(value, _base_path)
	value = BB_Text.transcode(value, _base_path)
	value = BB_IndentAndDot.transcode(value, _base_path)
	value = BB_Link.transcode(value, _base_path)
	value = BB_Image.transcode(value, _base_path)
	value = BB_Table.transcode(value, _base_path)
	value = BB_Code.transcode(value, _base_path)
	value = BB_Specification.transcode(value, _base_path)
	value = BB_lineReturn.transcode(value, _base_path)
	return value

##
## @brief transcode a BBcode file in a html file
## @return True if the file is transformed
##
def transcode_file(inputFileName, outputFileName):
	inData = tools.file_read_data(inputFileName)
	if inData == "":
		return False
	outData = transcode(inData)
	debug.warning(" out: " + outputFileName)
	tools.file_write_data(outputFileName, outData)
	return True


