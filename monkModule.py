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
import re

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
		self.listTutorialFile = []
		self.webSite = ""
		self.webSource = ""
		self.pathParsing = ""
		self.pathGlobalDoc = ""
		self.externalLink = []
		self.title = moduleName + " Library"
		self.styleHtml = ""
		## end of basic INIT ...
		if moduleType.upper() == 'APPLICATION':
			self.type = 'application'
		elif moduleType.upper() == 'LIBRARY':
			self.type = "library"
		else :
			debug.error('for module "%s"' %moduleName)
			debug.error('    ==> error : "%s" ' %moduleType)
			raise 'Input value error'
		self.structureLib = Node.MainNode(self.type, moduleName)
		self.originFile = file;
		self.originFolder = tools.get_current_path(self.originFile)
		
	
	
	##
	## @brief Set the module website (activate only when compile in release mode, else "../moduleName/)
	## @param[in] url New Website url
	##
	def set_website(self, url):
		self.webSite = url
	
	def get_website(self):
		return self.webSite
	
	def set_website_sources(self, url):
		self.webSource = url
	
	def get_website_sources(self):
		return self.webSource
	
	
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
		# all file is parset ==> now we create the namespacing of all elements:
		self.structureLib.set_namespace()
		self.structureLib.set_module_link(self)
		#self.structureLib.complete_display()
		
		# display the hierarchie of all the class and namespace ...
		#self.structureLib.debug_display()
		if self.pathGlobalDoc != "":
			for root, dirnames, filenames in os.walk(self.pathGlobalDoc):
				tmpList = fnmatch.filter(filenames, "*.bb")
				# Import the module :
				for filename in tmpList:
					fileCompleteName = os.path.join(root, filename)
					tutorialPath = os.path.join(self.pathGlobalDoc, "tutorial/")
					pathBase = fileCompleteName[len(self.pathGlobalDoc):len(fileCompleteName)-3]
					debug.verbose("    Find a doc file : fileCompleteName='" + fileCompleteName + "'")
					if fileCompleteName[:len(tutorialPath)] == tutorialPath:
						self.add_tutorial_doc(fileCompleteName, pathBase)
					else:
						self.add_file_doc(fileCompleteName, pathBase)
	
	##
	## @brief Add a documentation file at the parsing system
	## @param[in] filename File To add at the parsing element system.
	## @param[in] outPath output system file.
	## @return True if no error occured, False otherwise
	##
	def add_file_doc(self, filename, outPath):
		debug.debug("adding file in documantation : '" + filename + "'");
		done = False
		for iii in range(0,len(self.listDocFile)):
			if self.listDocFile[iii][0] > filename:
				self.listDocFile.insert(iii, [filename, outPath])
				done = True
				break
		if done == False:
			self.listDocFile.append([filename, outPath])
	
	##
	## @brief Add a documentation file at the parsing system
	## @param[in] filename File To add at the parsing element system.
	## @param[in] outPath output system file.
	## @return True if no error occured, False otherwise
	##
	def add_tutorial_doc(self, filename, outPath):
		count = int(filename.split('/')[-1].split('_')[0])
		debug.debug("adding file in documantation : '" + filename + "'");
		done = False
		for iii in range(0,len(self.listTutorialFile)):
			if self.listTutorialFile[iii][0] > filename:
				self.listTutorialFile.insert(iii, [filename, outPath])
				done = True
				break
		if done == False:
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
		tools.remove_folder_and_sub_folder(destFolder);
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
	
	def get_whith_specific_parrent(self, name, appName=None):
		if self.structureLib.get_node_type() == "library":
			return self.structureLib.get_whith_specific_parrent(name)
		if appName != self.structureLib.get_name():
			return []
		return self.structureLib.get_whith_specific_parrent(name)
	
	

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

