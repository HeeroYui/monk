#!/usr/bin/python
import monkDebug as debug
import sys
import monkTools
#import CppHeaderParser
import re
import codeBB
import collections

global_class_link = {
	"std::string"    : "http://www.cplusplus.com/reference/string/string/",
	"std::u16string" : "http://www.cplusplus.com/reference/string/u16string/",
	"std::u32string" : "http://www.cplusplus.com/reference/string/u32string/",
	"std::wstring"   : "http://www.cplusplus.com/reference/string/wstring/",
	"std::vector"    : "http://www.cplusplus.com/reference/vector/vector/"
	}

def display_color(val):
	# storage keyword :
	val = re.sub(r'(inline|const|class|virtual|private|public|protected|friend|const|extern|auto|register|static|volatile|typedef|struct|union|enum)',
	             r'<span class="code-storage-keyword">\1</span>',
	             val)
	# type :
	val = re.sub(r'(bool|BOOL|char(16_t|32_t)?|double|float|u?int(8|16|32|64|128)?(_t)?|long|short|signed|size_t|unsigned|void|(I|U)(8|16|32|64|128))',
	             r'<span class="code-type">\1</span>',
	             val)
	return val


def display_doxygen_param(comment, input, output):
	data = "<b>Parameter"
	if input == True:
		data += " [input]"
	if output == True:
		data += " [output]"
	data += ":</b> "
	#extract first element:
	val = comment.find(" ")
	var = comment[:val]
	endComment = comment[val:]
	# TODO : Check if it exist in the parameter list ...
	data += "<span class=\"code-argument\">" + var + "</span> " + endComment
	
	data += "<br/>"
	return data


def parse_doxygen(data) :
	streams = data.split("@")
	data2 = ''
	for element in streams:
		if    element[:1] == "\n" \
		   or element[:2] == "\n\n":
			# nothing to do : Nomale case of the first \n
			None
		elif element[:6] == "brief ":
			data2 += element[6:]
			data2 += "<br/>"
	
	for element in streams:
		if    element[:1] == "\n" \
		   or element[:2] == "\n\n":
			# nothing to do : Nomale case of the first \n
			None
		elif element[:5] == "note ":
			data2 += "<b>Notes:</b> "
			data2 += element[5:]
			data2 += "<br/> "
	
	data3 = ''
	for element in streams:
		if    element[:1] == "\n" \
		   or element[:2] == "\n\n":
			# nothing to do : Nomale case of the first \n
			None
		elif    element[:14] == "param[in,out] " \
		     or element[:14] == "param[out,in] ":
			data3 += display_doxygen_param(element[14:], True, True)
		elif element[:10] == "param[in] ":
			data3 += display_doxygen_param(element[10:], True, False)
		elif element[:11] == "param[out] ":
			data3 += display_doxygen_param(element[11:], False, True)
		elif element[:6] == "param ":
			data3 += display_doxygen_param(element[6:], False, False)
		elif element[:7] == "return ":
			data3 += "<b>Return:</b> "
			data3 += element[7:]
			data3 += "<br/>"
	if data3 != '':
		data2 += "<ul>\n"
		data2 += data3
		data2 += "</ul>\n"
	return data2

def white_space(size) :
	ret = ''
	for iii in range(len(ret), size):
		ret += " "
	return ret

def generate_menu(element, level=1):
	namespaceStack = element.get_namespace()
	listBase = element.get_all_sub_type(['namespace'])
	if len(listBase) == 0:
		return ""
	ret = ""
	ret += '<ul class="niveau' + str(level) + '">\n'
	for element in listBase:
		retTmp = generate_menu(element['node'], level+1)
		if retTmp != "":
			subMenu = ' class="sousmenu"'
		else:
			subMenu = ''
		ret += '	<li' + subMenu + '>' + generate_link(element['node']) + '\n'
		ret += retTmp
		ret += '	</li>\n'
	ret += '</ul>\n'
	return ret

def generate_html_page_name(element):
	return element.get_doc_website_page_local()

def generate_name(element):
	namespaceStack = element.get_namespace()
	link = ""
	for name in namespaceStack:
		link += name + "::"
	return element.get_node_type() + ": " + link + element.get_name()


def generate_link(element):
	return '<a href="' + generate_html_page_name(element) + '">' + element.get_name() + '</a>'

def calculate_methode_size(list):
	returnSize = 0;
	methodeSize = 0;
	for element in list:
		retType = ""
		if element['node'].get_virtual() == True:
			retType += 'virtual '
		retType += element['node'].get_return_type().to_str()
		tmpLen = len(retType)
		if returnSize < tmpLen:
			returnSize = tmpLen
		tmpLen = len(element['node'].get_name())
		if methodeSize < tmpLen:
			methodeSize = tmpLen
	return [returnSize, methodeSize]


def write_methode(element, namespaceStack, displaySize = None, link = True):
	if displaySize == None:
		displaySize = calculate_methode_size([element])
	ret = ""
	if 'access' in element.keys():
		if element['access'] == 'private':
			ret += '- '
		elif element['access'] == 'protected':
			ret += '# '
		elif element['access'] == 'public':
			ret += '+ '
		else:
			ret += '  '
	retType = ""
	if element['node'].get_virtual() == True:
		retType += 'virtual '
	retType += element['node'].get_return_type().to_str()
	if retType != "":
		retType2 = re.sub("<","&lt;", retType)
		retType2 = re.sub(">","&gt;", retType2)
		retType2 = display_color(retType2)
		ret += retType2
		ret += " "
		retType += " "
	ret += white_space(displaySize[0] - len(retType)+1)
	name = element['node'].get_name()
	if link == True:
		ret += '<a class="code-function" href="#' + str(element['node'].get_uid()) + '">' + name + '</a>'
	else:
		ret += '<span class="code-function">' + name + '</span>'
	ret += white_space(displaySize[1] - len(name)) + ' ('
	listParam = element['node'].get_param()
	first = True
	for param in listParam:
		if first == False:
			ret += ',<br/>'
			ret += white_space(displaySize[0] + displaySize[1] +5)
		first = False
		retParam = display_color(param.get_type().to_str())
		if retParam != "":
			ret += retParam
			ret += " "
		ret += "<span class=\"code-argument\">" + param.get_name() + "</span>"
	ret += ')'
	if element['node'].get_virtual_pure() == True:
		ret += ' = 0'
	if element['node'].get_constant() == True:
		ret += display_color(' const')
	
	ret += ';'
	ret += '<br/>'
	return ret

def generate_stupid_index_page(outFolder, header, footer, myLutinDoc):
	# create index.hml : 
	filename = outFolder + "/index.html"
	monkTools.create_directory_of_file(filename);
	file = open(filename, "w")
	file.write(header)
	file.write("<h1>" + myLutinDoc.get_base_doc_node().get_name() + "</h1>");
	file.write("<br/>");
	file.write("TODO : Main page ...");
	file.write("<br/>");
	file.write("<br/>");
	file.write(footer)
	file.close();

def generate_page(outFolder, header, footer, element):
	namespaceStack = element.get_namespace()
	if element.get_node_type() in ['library', 'application', 'namespace', 'class', 'struct', 'enum', 'union']:
		listBase = element.get_all_sub_type(['library', 'application', 'namespace', 'class', 'struct', 'enum', 'union'])
		for elem in listBase:
			generate_page(outFolder, header, footer, elem['node'])
	filename = outFolder + '/' + generate_html_page_name(element)
	monkTools.create_directory_of_file(filename);
	file = open(filename, "w")
	file.write(header)
	file.write('<h1>' + generate_name(element) + '</h1>');
	file.write('<hr/>');
	
	documentation = parse_doxygen(element.get_doc())
	if len(documentation) != 0:
		file.write('<h2>Description:</h2>\n')
		file.write(documentation)
		file.write('<br/>\n')
	
	if element.get_node_type() in ['library', 'application', 'namespace', 'class', 'struct']:
		for nameElement in ['namespace', 'class', 'struct', 'enum', 'union']:
			listBase = element.get_all_sub_type(nameElement)
			if len(listBase) == 0:
				continue
			file.write('<h2>' + nameElement + ':</h2>\n');
			file.write('<ul>\n');
			for elem in listBase:
				file.write('<li>' + generate_link(elem['node']) + '</li>')
			file.write('</ul>\n');
		
	# calculate element size :
	listBase = element.get_all_sub_type(['methode', 'constructor', 'destructor'])
	displayLen = calculate_methode_size(listBase)
	
	if    element.get_node_type() == 'class' \
	   or element.get_node_type() == 'struct':
		
		if len(element.get_all_sub_type(['constructor', 'destructor'])) != 0:
			file.write('<h2>Constructor and Destructor:</h2>\n')
			file.write('<pre>\n');
			listBaseConstructor = element.get_all_sub_type(['constructor'])
			for elem in listBaseConstructor:
				ret = write_methode(elem, namespaceStack, displayLen)
				file.write(ret)
			listBaseDestructor = element.get_all_sub_type(['destructor'])
			for elem in listBaseDestructor:
				ret = write_methode(elem, namespaceStack, displayLen)
				file.write(ret)
			file.write('</pre>\n');
			file.write('<br/>\n')
		
	if element.get_node_type() in ['library', 'application', 'namespace', 'class', 'struct']:
		listBaseMethode = element.get_all_sub_type(['methode'])
		if len(listBaseMethode) != 0:
			file.write('<h2>Synopsis:</h2>\n')
			file.write('<pre>\n');
			displayLen = calculate_methode_size(listBaseMethode)
			for elem in listBaseMethode:
				ret = write_methode(elem, namespaceStack, displayLen)
				file.write(ret)
			file.write('</pre>\n')
			file.write('<br/>\n')
	
	# generate herirage list :
	if element.get_node_type() == 'class':
		parent = element.get_parents()
		debug.verbose("parrent of " + element.get_name() + " : " + str(parent))
		child = None
		if len(parent) != 0:
			file.write('<h2>Object Hierarchy:<h2>\n')
			file.write('<pre>\n');
			level = 0
			revertList = []
			for elemmm in reversed(parent):
				revertList.append(elemmm)
			revertList.append({'access':'me', 'class':element.get_displayable_name()})
			for parentElem in revertList:
				access = ""
				if parentElem['access'] == 'public':
					access = "+"
				elif parentElem['access'] == 'protected':
					access = "#"
				elif parentElem['access'] == 'private':
					access = "-"
				file.write(white_space(level * 4))
				if level != 0:
					file.write('+--> ')
				file.write(access + parentElem['class'] + '<br/>')
				level += 1
			file.write('</pre>\n');
		
	
	if len(listBase) != 0:
		# display all functions :
		file.write('<h2>Detail:<h2>\n')
		for subElement in listBase:
			file.write('<h3><a id="' + str(subElement['node'].get_uid()) + '">' + subElement['node'].get_name() + '</a></h3>')
			file.write('<pre>\n');
			file.write(write_methode(subElement, namespaceStack, link = False))
			file.write('</pre>\n');
			#debug.info(str(element['node'].get_doc()));
			file.write(parse_doxygen(subElement['node'].get_doc()));
			file.write('<br/>\n');
			file.write('<hr/>\n');
		
	if element.get_node_type() == 'enum':
		myElementList = element.get_enum_list()
		elementSize = 0
		for enumElement in myElementList:
			tmpLen = len(enumElement['name'])
			if tmpLen > elementSize:
				elementSize = tmpLen
		
		
		file.write('<h2>Value list</h2>\n')
		if len(myElementList) < 9:
			nbColumn = 1
		else:
			nbColumn = 3
		
		file.write('<ul>\n');
		file.write('<table class="enumeration-list"><tr>\n');
		nbCol = 0
		isFirst = True
		for enumElement in myElementList:
			if isFirst == True:
				file.write('<tr>\n');
			isFirst = False
			file.write('<td><a href="#' + enumElement['name'] + '">' + enumElement['name'] + '</a></td>')
			nbCol += 1
			if nbCol == nbColumn:
				nbCol = 0
				file.write('</tr>\n');
				isFirst = True
		if isFirst == False:
			file.write('</tr>\n');
		file.write('</table>\n');
		file.write('</ul>\n');
		
		file.write("<h2>Detail:<h2>\n")
		isFirst = True
		for enumElement in myElementList:
			if isFirst == False:
				file.write('<hr/>\n');
			isFirst = False
			file.write('<a id="' + enumElement['name'] + '"/>' + enumElement['name'])
			file.write('<pre>\n')
			file.write(enumElement['name'] + white_space(elementSize-len(enumElement['name'])) + ' = <span class="code-type">' + enumElement['value'] + '<span>')
			file.write('</pre>\n')
			if enumElement['doc'] != "":
				file.write(parse_doxygen(enumElement['doc']));
		
	if element.get_node_type() == 'union':
		file.write("TODO : the page ...");
	
	file.write(footer)
	file.close();
	




def generate(myLutinDoc, outFolder) :
	myDoc = myLutinDoc.get_base_doc_node()
	monkTools.copy_file(monkTools.get_current_path(__file__)+"/theme/base.css", outFolder+"/base.css")
	monkTools.copy_file(monkTools.get_current_path(__file__)+"/theme/menu.css", outFolder+"/menu.css")
	# create common header
	genericHeader  = '<!DOCTYPE html>\n'
	genericHeader += '<html>\n'
	genericHeader += '<head>\n'
	genericHeader += '	<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">\n'
	genericHeader += '	<title>' + myDoc.get_name() + ' Library</title>\n'
	genericHeader += '	<link rel="stylesheet" href="base.css">\n'
	genericHeader += '	<link rel="stylesheet" href="menu.css">\n'
	genericHeader += '</head>\n'
	genericHeader += '<body>\n'
	genericHeader += '	<div class="navbar navbar-fixed-top">\n'
	genericHeader += '		<div class="container">\n'
	genericHeader += '			<h1>' + myDoc.get_name() + ' Library</h1>\n'
	genericHeader += '			<div id="menu">\n'
	#genericHeader += '				<h2>' + myDoc.moduleName + '</h2>\n'
	genericHeader += generate_menu(myDoc)
	#genericHeader += '				<h3> </h3>\n'
	genericHeader += '			</div>\n'
	genericHeader += "		</div>\n"
	genericHeader += "	</div>\n"
	genericHeader += "	<div class=\"container\" id=\"content\">\n"
	
	genericFooter  = "	</div>\n"
	genericFooter += "</body>\n"
	genericFooter += "</html>\n"
	
	# create index.hml : 
	generate_stupid_index_page(outFolder, genericHeader, genericFooter, myLutinDoc)
	
	# create the namespace index properties :
	generate_page(outFolder, genericHeader, genericFooter, myDoc)
	
	for docInputName,outpath in myLutinDoc.listDocFile :
		debug.print_element("doc", myLutinDoc.name, "<==", docInputName)
		outputFileName = outFolder + "/" + outpath.replace('/','_') +".html"
		debug.debug("output file : " + outputFileName)
		monkTools.create_directory_of_file(outputFileName)
		inData = monkTools.file_read_data(docInputName)
		if inData == "":
			continue
		outData = genericHeader + codeBB.transcode(inData) + genericFooter
		monkTools.file_write_data(outputFileName, outData)
	
	for docInputName,outpath in myLutinDoc.listTutorialFile :
		debug.print_element("tutorial", myLutinDoc.name, "<==", docInputName)
		outputFileName = outFolder + "/" + outpath+".html"
		debug.debug("output file : " + outputFileName)
		monkTools.create_directory_of_file(outputFileName)
		inData = monkTools.file_read_data(docInputName)
		if inData == "":
			continue
		outData = genericHeader + codeBB.transcode(inData) + genericFooter
		monkTools.file_write_data(outputFileName, outData)



