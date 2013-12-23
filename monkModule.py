#!/usr/bin/python
import sys
import os
import inspect
import fnmatch
import monkDebug as debug
import monkTools as tools
import monkNode as Node
import monkParse as Parse
import monkHtml

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
		self.originFile=''
		self.originFolder=''
		# type of the module:
		self.type='LIBRARY'
		# Name of the module
		self.name=moduleName
		self.listDocFile = []
		self.structureLib = Node.MainNode("library", moduleName)
		self.listTutorialFile = []
		self.webSite = ""
		self.pathParsing = ""
		self.pathGlobalDoc = ""
		self.externalLink = []
		self.title = moduleName + " Library"
		self.styleHtml = ""
		## end of basic INIT ...
		if    moduleType == 'APPLICATION' \
		   or moduleType == 'LIBRARY':
			self.type=moduleType
		else :
			debug.error('for module "%s"' %moduleName)
			debug.error('    ==> error : "%s" ' %moduleType)
			raise 'Input value error'
		self.originFile = file;
		self.originFolder = tools.get_current_path(self.originFile)
		
	
	
	##
	## @brief Set the module website (activate only when compile in release mode, else "../moduleName/)
	## @param[in] url New Website url
	##
	def set_website(self, url):
		self.webSite = url
	
	##
	## @brief set the parsing folder
	## @param[in] path New path to parse
	##
	def set_path(self, path):
		self.pathParsing = path
	
	##
	## @brief set the glabal documentation parsing folder
	## @param[in] path New path to parse
	##
	def set_path_general_doc(self, path):
		self.pathGlobalDoc = path
	
	##
	## @brief List of validate external library link (disable otherwise)
	## @param[in] availlable List of all module link availlable 
	##
	def set_external_link(self, availlable):
		self.externalLink = availlable
	
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
		self.styleHtml = cssFile
	
	##
	## @brief Create the module documentation:
	##
	def parse_code(self):
		debug.info('Parse documantation code : ' + self.name)
		if self.pathParsing != "":
			for root, dirnames, filenames in os.walk(self.pathParsing):
				tmpList = fnmatch.filter(filenames, "*.h")
				# Import the module :
				for filename in tmpList:
					fileCompleteName = os.path.join(root, filename)
					debug.debug("    Find a file : '" + fileCompleteName + "'")
					self.add_file(fileCompleteName)
		# display the hierarchie of all the class and namespace ...
		#self.structureLib.debug_display()
		if self.pathGlobalDoc != "":
			for root, dirnames, filenames in os.walk(self.pathGlobalDoc):
				tmpList = fnmatch.filter(filenames, "*.bb")
				# Import the module :
				for filename in tmpList:
					fileCompleteName = os.path.join(root, filename)
					tutorialPath = os.path.join(self.pathGlobalDoc, "tutorial/")
					debug.verbose("    Find a doc file : '" + fileCompleteName + "'")
					pathBase = fileCompleteName[len(self.pathGlobalDoc):len(fileCompleteName)-3]
					if fileCompleteName[:len(tutorialPath)] == tutorialPath:
						self.add_file_doc(fileCompleteName, pathBase)
					else:
						self.add_tutorial_doc(fileCompleteName, pathBase)
	
	##
	## @brief Add a documentation file at the parsing system
	## @param[in] filename File To add at the parsing element system.
	## @param[in] outPath output system file.
	## @return True if no error occured, False otherwise
	##
	def add_file_doc(self, filename, outPath):
		debug.debug("adding file in documantation : '" + filename + "'");
		self.listDocFile.append([filename, outPath])
	
	##
	## @brief Add a documentation file at the parsing system
	## @param[in] filename File To add at the parsing element system.
	## @param[in] outPath output system file.
	## @return True if no error occured, False otherwise
	##
	def add_tutorial_doc(self, filename, outPath):
		debug.debug("adding file in documantation : '" + filename + "'");
		self.listTutorialFile.append([filename, outPath])
	
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
		self.structureLib = parsedFile.fusion(self.structureLib)
		
		return True
	
	##
	## @brief Generate Documentation at the folder ...
	## @param[in] destFolder Destination folder.
	## @param[in] mode (optinnal) generation output mode {html, markdown ...}
	##
	def generate(self):
		debug.info('Generate documantation code : ' + self.name)
		destFolder = "out/doc/" + self.name + '/'
		#tools.remove_folder_and_sub_folder(target.get_doc_folder(self.name));
		if monkHtml.generate(self, destFolder) == False:
			debug.warning("Generation Documentation ==> return an error for " + self.name)
		
	
	def get_base_doc_node(self):
		return self.structureLib
	
	##
	## @brief Get the heritage list (parent) of one element.
	## @param[in] element Element name.
	## @return List of all element herited
	##
	def get_heritage_list(self, element):
		list = []
		# get element class :
		if element in self.listClass.keys():
			localClass = self.listClass[element]
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
		for element in self.listClass:
			localClass = self.listClass[element]
			if len(localClass['inherits']) != 0:
				for heritedClass in localClass['inherits']:
					if curentClassName == heritedClass['class']:
						list.append(element)
						break;
		debug.verbose("find childs : " + str(list))
		return list
	
	##
	## @brief trnsform the classname in a generic link (HTML)
	## @param[in] elementName Name of the class requested
	## @return [className, link]
	##
	def get_class_link(self, elementName):
		if    elementName == "const" \
		   or elementName == "enum" \
		   or elementName == "void" \
		   or elementName == "char" \
		   or elementName == "char32_t" \
		   or elementName == "float" \
		   or elementName == "double" \
		   or elementName == "bool" \
		   or elementName == "int8_t" \
		   or elementName == "uint8_t" \
		   or elementName == "int16_t" \
		   or elementName == "uint16_t" \
		   or elementName == "int32_t" \
		   or elementName == "uint32_t" \
		   or elementName == "int64_t" \
		   or elementName == "uint64_t" \
		   or elementName == "int" \
		   or elementName == "T" \
		   or elementName == "CLASS_TYPE" \
		   or elementName[:5] == "std::" \
		   or elementName[:6] == "appl::" \
		   or elementName == "&" \
		   or elementName == "*" \
		   or elementName == "**":
			return [elementName, ""]
		if elementName in self.listClass.keys():
			link = elementName.replace(":","_") + ".html"
			return [elementName, link]
		elif elementName in self.listEnum.keys():
			link = elementName.replace(":","_") + ".html"
			return [elementName, link]
		#else:
		#	return self.target.doc_get_link(elementName)
		return [elementName, ""]
	
	##
	## @brief trnsform the classname in a generic link (HTML) (external access ==> from target)
	## @param[in] elementName Name of the class requested
	## @return [className, link]
	##
	def get_class_link_from_target(self, elementName, target):
		# reject when auto call :
		if self.target != None:
			return [elementName, ""]
		# search in local list :
		if elementName in self.listClass.keys():
			link = elementName.replace(":","_") + ".html"
			if target.get_build_mode() == "debug":
				return [elementName, "../" + self.moduleName + "/" + link]
			elif self.webSite != "":
				return [elementName, self.webSite + "/" + link]
		elif elementName in self.listEnum.keys():
			link = elementName.replace(":","_") + ".html"
			if target.get_build_mode() == "debug":
				return [elementName, "../" + self.moduleName + "/" + link]
			elif self.webSite != "":
				return [elementName, self.webSite + "/" + link]
		# did not find :
		return [elementName, ""]
	
	
	
	
	
	
	
	
	
	
	##
	## @brief Get link on a class or an enum in all the subclasses
	## @param[in] name of the class
	## @return [real element name, link on it]
	##
	def doc_get_link(self, target, elementName):
		if self.documentation == None:
			return [elementName, ""]
		return self.documentation.get_class_link_from_target(elementName, target);
	
	def display(self, target):
		print '-----------------------------------------------'
		print ' package : "' + self.name + '"'
		print '-----------------------------------------------'
		print '    type:"%s"' %self.type
		print '    file:"%s"' %self.originFile
		print '    folder:"%s"' %self.originFolder
		self.print_list('local_path',self.local_path)
	

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

