#!/usr/bin/python
import sys
import os
import inspect
import fnmatch
from realog import debug
from . import tools
from . import monkNode as Node
from . import monkParse as Parse
from . import monkHtml
import re
import json

class Module:
	##
	## @brief Module class represent all system needed for a specific
	## 	module like 
	## 		- type (bin/lib ...)
	## 		- dependency
	## 		- flags
	## 		- files
	## 		- ...
	##
	def __init__(self, file, moduleName, moduleType):
		## Remove all variable to prevent error of multiple deffinition of the module ...
		self.origin_file=''
		self.origin_folder=''
		# type of the module:
		self.type='LIBRARY'
		# Name of the module
		self.name=moduleName
		self.list_doc_file = []
		self.list_image_file = []
		self.list_tutorial_file = []
		self.list_manual_file = []
		self.list_test_file = []
		self.web_site = ""
		self.web_source = ""
		self.path_parsing = ""
		self.path_global_doc = ""
		self.external_link = []
		self.title = moduleName + " Library"
		self.style_html = ""
		## end of basic INIT ...
		if moduleType.upper() == 'APPLICATION':
			self.type = 'application'
		elif moduleType.upper() == 'LIBRARY':
			self.type = "library"
		else :
			debug.error('for module "%s"' %moduleName)
			debug.error('    ==> error : "%s" ' %moduleType)
			raise 'Input value error'
		self.structure_lib = Node.MainNode(self.type, moduleName)
		self.origin_file = file;
		self.origin_folder = tools.get_current_path(self.origin_file)
		
	
	
	##
	## @brief Set the module web_site (activate only when compile in release mode, else "../moduleName/)
	## @param[in] url New web_site url
	##
	def set_website(self, url):
		self.web_site = url
	
	def get_website(self):
		return self.web_site
	
	def set_website_sources(self, url):
		self.web_source = url
	
	def get_website_sources(self):
		return self.web_source
	
	
	##
	## @brief set the parsing folder
	## @param[in] path New path to parse
	##
	def set_path(self, path):
		self.path_parsing = path
	
	##
	## @brief set the glabal documentation parsing folder
	## @param[in] path New path to parse
	##
	def set_path_general_doc(self, path):
		self.path_global_doc = path
	
	##
	## @brief List of validate external library link (disable otherwise)
	## @param[in] availlable List of all module link availlable 
	##
	def set_external_link(self, availlable):
		self.external_link = availlable
	
	##
	## @brief Set the library title
	## @param[in] title New title to set.
	##
	def set_title(self, title):
		self.title = title
	
	##
	## @brief new html basic css file
	## @param[in] file File of the css style sheet
	##
	def set_html_css(self, cssFile):
		self.style_html = cssFile
	
	##
	## @brief Create the module documentation:
	##
	def parse_code(self):
		debug.info('Parse documantation code : ' + self.name)
		if self.path_parsing != "":
			for root, dirnames, filenames in os.walk(self.path_parsing):
				tmpList = fnmatch.filter(filenames, "*.hpp")
				# Import the module :
				for filename in tmpList:
					file_complete_name = os.path.join(root, filename)
					debug.debug("    Find a file : '" + file_complete_name + "'")
					self.add_file(file_complete_name)
		# all file is parset ==> now we create the namespacing of all elements:
		self.structure_lib.set_namespace()
		self.structure_lib.set_module_link(self)
		#self.structure_lib.complete_display()
		
		# display the hierarchie of all the class and namespace ...
		#self.structure_lib.debug_display()
		if self.path_global_doc != "":
			for root, dirnames, filenames in os.walk(self.path_global_doc):
				tmpList = fnmatch.filter(filenames, "*.md")
				# Import the module :
				for filename in tmpList:
					file_complete_name = os.path.join(root, filename)
					tutorial_path = os.path.join(self.path_global_doc, "tutorial/")
					test_path = os.path.join(self.path_global_doc, "test/")
					manual_path = os.path.join(self.path_global_doc, "manual/")
					path_base = file_complete_name[len(self.path_global_doc):len(file_complete_name)-3]
					while     len(path_base) > 0 \
					      and path_base[0] == '/':
						path_base = path_base[1:]
					debug.verbose("    Find a doc file : file_complete_name='" + file_complete_name + "'")
					if file_complete_name[:len(tutorial_path)] == tutorial_path:
						debug.warning("add_tutorial_doc : '" + file_complete_name + "' ==> '" + path_base + "'")
						self.add_tutorial_doc(file_complete_name, path_base)
					elif file_complete_name[:len(test_path)] == test_path:
						debug.warning("add_test_doc : '" + file_complete_name + "' ==> '" + path_base + "'")
						self.add_test_doc(file_complete_name, path_base)
					elif file_complete_name[:len(manual_path)] == manual_path:
						debug.warning("add_user_manual_doc : '" + file_complete_name + "' ==> '" + path_base + "'")
						self.add_user_manual_doc(file_complete_name, path_base)
					else:
						debug.warning("add_file_doc : '" + file_complete_name + "' ==> '" + path_base + "'")
						self.add_file_doc(file_complete_name, path_base)
			for root, dirnames, filenames in os.walk(self.path_global_doc):
				for filename in filenames:
					if not filename.endswith(('.jpg', '.JPG', '.jpeg', '.JPEG', '.png', '.PNG', '.svg', '.SVG', '.gif', '.GIF', '.tga', '.TGA')):
						continue
					file_complete_name = os.path.join(root, filename)
					path_base = file_complete_name[len(self.path_global_doc)+1:]
					debug.verbose("    Find a doc file : file_complete_name='" + file_complete_name + "'")
					debug.warning("add_image_doc: '" + file_complete_name + "' ==> '" + path_base + "'")
					self.add_image_doc(file_complete_name, path_base)
	
	##
	## @brief Sort a list of n element containing a list of element (order with the first)
	## @param[in] value List to order
	## @return ordered list
	##
	def sort_list_first_elem(self, value):
		# order the list:
		order_elem = []
		for elem in value:
			order_elem.append(elem[0])
		order_elem.sort()
		out = []
		for elem in order_elem:
			for old_val in value:
				if elem == old_val[0]:
					out.append(old_val)
					break;
		return out
	
	##
	## @brief Add a documentation file at the parsing system
	## @param[in] filename File To add at the parsing element system.
	## @param[in] outPath output system file.
	## @return True if no error occured, False otherwise
	##
	def add_file_doc(self, filename, outPath):
		debug.debug("adding file in documantation : '" + filename + "'");
		done = False
		for iii in range(0,len(self.list_doc_file)):
			if self.list_doc_file[iii][0] > filename:
				self.list_doc_file.insert(iii, [filename, outPath])
				done = True
				break
		if done == False:
			self.list_doc_file.append([filename, outPath])
		self.list_doc_file = self.sort_list_first_elem(self.list_doc_file)
	
	##
	## @brief Add a documentation image file to copy to the output
	## @param[in] filename File To add in the output documentation.
	## @param[in] outPath output system file.
	## @return True if no error occured, False otherwise
	##
	def add_image_doc(self, filename, outPath):
		debug.debug("adding file in documantation : '" + filename + "'");
		done = False
		for iii in range(0,len(self.list_image_file)):
			if self.list_image_file[iii][0] > filename:
				self.list_image_file.insert(iii, [filename, outPath])
				done = True
				break
		if done == False:
			self.list_image_file.append([filename, outPath])
		self.list_image_file = self.sort_list_first_elem(self.list_image_file)
	
	##
	## @brief Add a documentation file at the parsing system
	## @param[in] filename File To add at the parsing element system.
	## @param[in] outPath output system file.
	## @return True if no error occured, False otherwise
	##
	def add_tutorial_doc(self, filename, outPath):
		#count = int(filename.split('/')[-1].split('_')[0])
		debug.debug("adding file in documantation : '" + filename + "'");
		done = False
		for iii in range(0,len(self.list_tutorial_file)):
			if self.list_tutorial_file[iii][0] > filename:
				self.list_tutorial_file.insert(iii, [filename, outPath])
				done = True
				break
		if done == False:
			self.list_tutorial_file.append([filename, outPath])
		self.list_tutorial_file = self.sort_list_first_elem(self.list_tutorial_file)
		
	
	##
	## @brief Add a documentation file at the parsing system
	## @param[in] filename File To add at the parsing element system.
	## @param[in] outPath output system file.
	## @return True if no error occured, False otherwise
	##
	def add_user_manual_doc(self, filename, outPath):
		#count = int(filename.split('/')[-1].split('_')[0])
		debug.debug("adding file in user manual documantation : '" + filename + "'");
		done = False
		for iii in range(0,len(self.list_tutorial_file)):
			if self.list_manual_file[iii][0] > filename:
				self.list_manual_file.insert(iii, [filename, outPath])
				done = True
				break
		if done == False:
			self.list_manual_file.append([filename, outPath])
		self.list_manual_file = self.sort_list_first_elem(self.list_manual_file)
		
	##
	## @brief Add a documentation file at the parsing system
	## @param[in] filename File To add at the parsing element system.
	## @param[in] outPath output system file.
	## @return True if no error occured, False otherwise
	##
	def add_test_doc(self, filename, outPath):
		#count = int(filename.split('/')[-1].split('_')[0])
		debug.debug("adding file in test documantation : '" + filename + "'");
		done = False
		for iii in range(0,len(self.list_tutorial_file)):
			if self.list_test_file[iii][0] > filename:
				self.list_test_file.insert(iii, [filename, outPath])
				done = True
				break
		if done == False:
			self.list_test_file.append([filename, outPath])
		self.list_test_file = self.sort_list_first_elem(self.list_test_file)
		
	
	##
	## @brief Add a file at the parsing system
	## @param[in] filename File To add at the parsing element system.
	## @return True if no error occured, False otherwise
	##
	def add_file(self, filename):
		debug.debug("adding file in documantation : '" + filename + "'");
		
		#parsedFile = Parse.parse_file("Widget.h")
		#debug.error("plop")
		parsedFile = Parse.parse_file(filename)
		self.structure_lib = parsedFile.fusion(self.structure_lib)
		
		return True
	
	##
	## @brief Generate Documentation at the folder ...
	## @param[in] destFolder Destination folder.
	## @param[in] mode (optinnal) generation output mode {html, markdown ...}
	##
	def generate(self):
		debug.info('Generate documantation code : ' + self.name)
		#json_data = json.dumps(self, sort_keys=True, indent=4)
		#tools.file_write_data(os.path.join("out", "doc", self.name + ".json"), json_data)
		destFolder = os.path.join("out", "doc", self.name)
		tools.remove_folder_and_sub_folder(destFolder);
		if monkHtml.generate(self, destFolder + '/') == False:
			debug.warning("Generation Documentation ==> return an error for " + self.name)
		
	
	def get_base_doc_node(self):
		return self.structure_lib
	
	##
	## @brief Get the heritage list (parent) of one element.
	## @param[in] element Element name.
	## @return List of all element herited
	##
	def get_heritage_list(self, element):
		list = []
		# get element class :
		if element in self.list_class.keys():
			localClass = self.list_class[element]
			if len(localClass['inherits']) != 0:
				# TODO : Support multiple heritage ...
				isFirst = True
				for heritedClass in localClass['inherits']:
					if isFirst == True:
						list = self.get_heritage_list(heritedClass['class'])
						break;
		debug.verbose("find parent : " + element)
		list.append(element);
		return list
	
	##
	## @brief Get the heritage list (child) of this element.
	## @param[in] curentClassName Element name.
	## @return List of all childs
	##
	def get_down_heritage_list(self, curentClassName):
		list = []
		# get element class :
		for element in self.list_class:
			localClass = self.list_class[element]
			if len(localClass['inherits']) != 0:
				for heritedClass in localClass['inherits']:
					if curentClassName == heritedClass['class']:
						list.append(element)
						break;
		debug.verbose("find childs : " + str(list))
		return list
	
	def get_whith_specific_parrent(self, name, appName=None):
		if self.structure_lib.get_node_type() == "library":
			return self.structure_lib.get_whith_specific_parrent(name)
		if appName != self.structure_lib.get_name():
			return []
		return self.structure_lib.get_whith_specific_parrent(name)
	
	

moduleList=[]
__startModuleName="monk_"

def import_path(path):
	global moduleList
	matches = []
	debug.debug('Start find sub File : "%s"' %path)
	for root, dirnames, filenames in os.walk(path):
		tmpList = fnmatch.filter(filenames, __startModuleName + "*.py")
		# Import the module :
		for filename in tmpList:
			debug.debug('    Find a file : "%s"' %os.path.join(root, filename))
			#matches.append(os.path.join(root, filename))
			sys.path.append(os.path.dirname(os.path.join(root, filename)) )
			moduleName = filename.replace('.py', '')
			moduleName = moduleName.replace(__startModuleName, '')
			debug.debug("integrate module: '" + moduleName + "' from '" + os.path.join(root, filename) + "'")
			theModule = __import__(__startModuleName + moduleName)
			tmpElement = theModule.create()
			try:
				tmpdesc = theModule.get_desc()
			except:
				tmpdesc = ""
			if (tmpElement == None) :
				debug.warning("Request load module '" + name + "' not define for this platform")
			moduleList.append({"name":moduleName, "path":os.path.join(root, filename), "node":tmpElement, "desc":tmpdesc})

def get_module(name):
	global moduleList
	for mod in moduleList:
		if mod["name"] == name:
			return mod["node"]
	return None

def get_all_module():
	global moduleList
	AllList = []
	for mod in moduleList:
		AllList.append(mod["node"])
	return AllList

def list_all_module_with_desc():
	global moduleList
	tmpList = []
	for mod in moduleList:
		tmpList.append([mod["name"], mod["desc"]])
	return tmpList

def get_link_type(type):
	return ""

def get_element_with_name(type):
	global moduleList
	debug.verbose("try find : " + str(type) + "  ")
	ret = re.sub(r'::', ':', type)
	ret = ret.split(":")
	for mod in moduleList:
		element = mod['node'].get_base_doc_node().find(ret)
		if element != None:
			debug.debug("we find : " + type + " = " + str(ret) + "   " + str(element))
			return element
	debug.debug("we not find : " + type + " = " + str(ret))
	return None

def get_whith_specific_parrent(name, appName=None):
	global moduleList
	ret = []
	for mod in moduleList:
		tmpRet = mod['node'].get_whith_specific_parrent(name, appName)
		if len(tmpRet) != 0:
			for tmp in tmpRet:
				ret.append(tmp)
	return ret



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

