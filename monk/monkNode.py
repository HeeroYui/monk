#!/usr/bin/python
from realog import debug
from . import module

access_list = ['private', 'protected', 'public']

def debug_space(level):
	ret = ""
	for iii in range(0,level):
		ret += "    "
	return ret

genericUID = 0

class Node():
	def __init__(self, type, name="", file="", line_number=0, documentation=[]):
		global genericUID
		genericUID+=1
		self.uid = genericUID
		self.documenatation_code = []
		self.node_type = type
		self.name = name
		self.doc = None
		self.file_name = file
		self.line_number = line_number
		self.sub_list = None
		self.access = None
		# namespace elements : (set when all element are parsed ...
		self.namespace = []
		self.module_link = None # this is a link on the main application node or library node (usefull to get the website ...)
		self.hidden_request = False # @not-in-doc
		self.previous_request = False # @previous
		self.template = []
		self.add_doc(documentation)
	
	def to_str(self):
		return ""
	
	def str(self):
		return self.to_str()
	
	def get_node_type(self):
		return self.node_type
	
	def get_name(self):
		ret = ""
		if self.template != []:
			ret += "template&lt;"
			first = True
			for elem in self.template:
				if first == True:
					first = False
				else:
					ret += ", "
				if len(elem) >= 2:
					ret += elem[1]
				else:
					ret += elem[0]
			ret += "&gt "
		ret += self.name
		return ret
	
	def get_UID(self):
		return self.uid
	
	def add_doc(self, doc):
		for element in doc:
			self.documenatation_code.append(element)
			if element.find("@not-in-doc") != -1 :
				self.hidden_request = True
			if element.find("@previous") != -1 :
				self.previous_request = True
			
	
	def get_request_hidden(self):
		return self.hidden_request
	
	def get_request_in_previous(self):
		return self.previous_request
	
	
	def get_displayable_name(self):
		ret = ""
		for namespace in self.namespace:
			ret += namespace + "::"
		ret += self.name
		return ret
	
	def get_uid(self):
		return self.uid
	
	def get_doc(self):
		#debug.info(str(self.doc))
		if len(self.documenatation_code) > 0:
			ret = ""
			isFirst = True
			for req in self.documenatation_code:
				if isFirst == False:
					ret += '\n'
				isFirst = False
				ret += req
			return ret
		if self.node_type not in ['methode']:
			return ""
		#try to get previous element : 
		if len(self.namespace) == 0:
			return ""
		parent = ""
		isFirst = True
		for namesapace in self.namespace:
			if isFirst == False:
				parent += "::"
			isFirst = False
			parent += namesapace
		element = module.get_element_with_name(parent)
		if element == None:
			return ""
		
		if element.get_node_type() != 'class':
			return ""
		
		parents = element.get_parents()
		if len(parents) == 0:
			return ""
		
		for myParent in reversed(parents):
			element = module.get_element_with_name(myParent[0]['class'])
			if element == None:
				continue
			heveMethode, pointerMethode = element.have_methode(self.name)
			if heveMethode == False:
				continue
			if len(pointerMethode.documenatation_code) != 0:
				return pointerMethode.get_doc()
		
		return ""
	
	def get_lib_name(self):
		if self.module_link == None:
			return None
		return self.module_link.get_base_doc_node().get_name()
	
	def debug_display(self, level=0, access = None):
		if access == 'private':
			debug.info(debug_space(level) + "- " + self.node_type + " => " + self.name)
		elif access == 'protected':
			debug.info(debug_space(level) + "# " + self.node_type + " => " + self.name)
		elif access == 'public':
			debug.info(debug_space(level) + "+ " + self.node_type + " => " + self.name)
		else:
			debug.info(debug_space(level) + self.node_type + " => " + self.name)
		if self.sub_list!= None:
			for element in self.sub_list:
				if 'access' in element.keys():
					element['node'].debug_display(level+1, element['access'])
				else:
					element['node'].debug_display(level+1)
	
	def set_access(self, access):
		if access not in access_list:
			debug.warning("This is not a valid access : '" + access + "' : availlable : " + str(access_list))
			return
		if self.access == None:
			debug.error("This Node does not support acces configuration...")
			return
		self.access = access
	
	def get_access(self):
		return self.access
	
	def append(self, newSubElement):
		# just add it in a sub List :
		if self.sub_list == None:
			debug.error("can not add a '" + newSubElement.node_type + "' at this '" + self.node_type + "'")
			return
		if newSubElement.get_node_type() != 'namespace':
			if self.access == None:
				self.sub_list.append({'node' : newSubElement})
			else:
				self.sub_list.append({'access' : self.access, 'node' : newSubElement})
			return
		
		# check if the element already exist
		for element in self.sub_list:
			if element['node'].get_node_type() == 'namespace':
				if element['node'].get_name() == newSubElement.get_name():
					debug.verbose("fusionate with previous declaration")
					element['node'].fusion(newSubElement)
					return
		# normal case adding :
		if self.access == None:
			self.sub_list.append({'node' : newSubElement})
		else:
			self.sub_list.append({'access' : self.access, 'node' : newSubElement})
	
	##
	## @ brief only for namespace :
	## 
	##
	def fusion(self, addedElement):
		for element in addedElement.sub_list:
			self.append(element['node'])
	
	##
	## @brief Get the list of all specify type
	## @param[in] type Type requested ['namespace', 'class', 'struct', 'methode', 'enum', 'define', 'union', 'variable', 'constructor', 'destructor'] (can be a list)
	## @param[in] sorted Request to sort the return list.
	## @return The requested list or []
	##
	def get_all_sub_type(self, type='all', sorted = False):
		if type == 'all':
			return self.sub_list
		if isinstance(type, list) == False:
			type = [type]
		if self.sub_list == None:
			return []
		ret = []
		for element in self.sub_list:
			if element['node'].get_node_type() in type:
				ret.append(element)
		if sorted == True:
			# TODO : Sorted the list ...
			pass
		return ret
	
	def get_doc_website_page(self):
		if self.module_link == None:
			return ""
		ret = self.module_link.get_website()
		if ret[-1] != '/':
			ret += '/'
		ret += self.get_node_type()
		ret += "_"
		for name in self.namespace:
			ret += name + "__"
		if self.name == "":
			ret += "NO_NAME_" + str(self.uid)
		else:
			ret += self.name
		ret += '.html'
		return ret
	
	def get_doc_website_page_local(self):
		ret = self.get_node_type()
		ret += "_"
		for name in self.namespace:
			ret += name + "__"
		if self.name == "":
			ret += "NO_NAME_" + str(self.uid)
		else:
			ret += self.name
		if self.template != []:
			ret += "__template_"
			first = True
			for elem in self.template:
				if first == True:
					first = False
				else:
					ret += "_"
				if len(elem) >= 2:
					ret += elem[1]
				else:
					ret += elem[0]
			ret += "__"
		ret += '.html'
		return ret
	
	def set_module_link(self, module):
		self.module_link = module
		# set for all sub elements ...
		if self.sub_list == None:
			return
		if self.node_type in ['class', 'namespace', 'struct']:
			for element in self.sub_list:
				element['node'].set_module_link(module)
		elif self.node_type in ['library', 'application']:
			for element in self.sub_list:
				element['node'].set_module_link(module)
	
	def set_namespace(self, hierarchy = []):
		#debug.info('set namespace : ' + self.name + ' : ' + str(hierarchy))
		# store namespaces:
		for tmpName in hierarchy:
			self.namespace.append(tmpName)
		# set for all sub elements ...
		if self.sub_list == None:
			return
		if self.node_type in ['class', 'namespace', 'struct']:
			for element in self.sub_list:
				hierarchy.append(self.name)
				element['node'].set_namespace(hierarchy)
				#debug.info(" ==> " + str(element['node'].get_namespace()))
				hierarchy.pop()
		elif self.node_type in ['library', 'application']:
			for element in self.sub_list:
				element['node'].set_namespace()
				#debug.info(" ==> " + str(element['node'].get_namespace()))
	
	def get_namespace(self):
		return self.namespace
	
	def complete_display(self):
		debug.info(str(self.namespace) + ' : ' + self.name)
		if self.sub_list == None:
			return
		for element in self.sub_list:
			element['node'].complete_display()
	
	def find(self, list):
		debug.verbose("find : " + str(list) + " in " + self.node_type + "(" + self.name + ")")
		if len(list) == 0:
			return None
		if self.node_type in ['library', 'application']:
			if self.sub_list == None:
				return None
			for element in self.sub_list:
				ret = element['node'].find(list)
				if ret != None:
					return ret
			return None
		if list[0] != self.name:
			return None
		tmpList = list[1:]
		if len(tmpList) == 0:
			return self
		elif self.node_type not in ['class', 'namespace', 'struct']:
			# have other sub element and other elemetn than upper can have sub element ...
			return None
		if self.sub_list == None:
			return None
		for element in self.sub_list:
			ret = element['node'].find(tmpList)
			if ret != None:
				return ret
		return None
	
	
	def get_whith_specific_parrent(self, parrentName):
		ret = []
		# set for all sub elements ...
		if self.sub_list != None:
			for element in self.sub_list:
				tmpRet = element['node'].get_whith_specific_parrent(parrentName)
				if len(tmpRet) != 0:
					for tmp in tmpRet:
						ret.append(tmp)
		return ret
	
	def have_methode(self, methodeName):
		if self.sub_list != None:
			for element in self.sub_list:
				if element['node'].get_node_type() != 'methode':
					continue
				if element['access'] == "private":
					continue
				if element['node'].get_virtual() == False:
					continue
				if element['node'].get_name() == methodeName:
					return [True, element['node']]
		return [False, None]


class MainNode(Node):
	def __init__(self, type="library", name=""):
		Node.__init__(self, type, name)
		self.sub_list = []

def get_doc_website_page_relative(base, dest):
	realBase = ""
	tmpBase = ""
	lastFolder = ""
	for element in base:
		tmpBase += element
		if element == '/':
			realBase += tmpBase
			lastFolder = tmpBase
			tmpBase = ""
	if dest[:len(realBase)] == realBase:
		return dest[len(realBase):]
	#debug.info(dest[:len(realBase)-len(lastFolder)] + "==" + realBase[:-len(lastFolder)])
	if dest[:len(realBase)-len(lastFolder)] == realBase[:-len(lastFolder)]:
		return '../' + dest[len(realBase)-len(lastFolder):]
	return dest


