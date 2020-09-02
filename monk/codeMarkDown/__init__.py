#!/usr/bin/python
from realog import debug
import sys
from monk import tools
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
import MD_Image
import MD_Code
import MD_Link
import MD_Table
import MD_ResultSelection
##
## @brief Transcode input data in the corect format.
## @param[in] string String to transform.
## @return Transformed string.
##
def transcode(value, _base_path = ""):
	# remove html property
	value = re.sub(r'&', r'&amp;', value)
	value = re.sub(r'<', r'&lt;', value)
	value = re.sub(r'>', r'&gt;', value)
	value = re.sub(r'\r\n', r'\n', value)
	value = re.sub(r'\n\r', r'\n', value)
	value = re.sub(r'\r', r'\n', value)
	value = MD_comment.transcode(value, _base_path)
	value = MD_Title.transcode(value, _base_path)
	value = MD_IndentAndDot.transcode(value, _base_path)
	value = MD_Code.transcode(value, _base_path)
	
	value = MD_Table.transcode(value, _base_path)
	value = MD_lineReturn.transcode(value, _base_path)
	value = MD_Title.transcode_clean_empty_line_after(value, _base_path)
	"""
	value = BB_Text.transcode(value, _base_path)
	value = BB_Specification.transcode(value, _base_path)
	"""
	value = MD_Image.transcode(value, _base_path)
	value = MD_Link.transcode(value, _base_path)
	value = MD_ResultSelection.transcode(value, _base_path)
	
	
	
	
	value = MD_Text.transcode(value, _base_path)
	
	
	
	
	value = MD_Code.transcode_part2(value)
	value = MD_Image.transcode_part2(value)
	value = MD_Link.transcode_part2(value)
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


