#!/usr/bin/python
import monkDebug as debug
import monkNode as Node
import monkModule as module


##
## @brief transform template descrption in one element.
## @param[in] list of elements. ex : 'public', 'ewol::classee', '<', 'plop', '<', 'uint8_t', ',', 'int32_t', '>', '>'
## @return a simplify list. ex : 'public', 'ewol::classee<plop<uint8_t,int32_t>>'
##
def concatenate_template(list):
	# TODO ...
	return list

class Class(Node.Node):
	def __init__(self, stack=[], file="", lineNumber=0, documentation=[]):
		# check input :
		if len(stack) < 2:
			debug.error("Can not parse class : " + str(stack))
			return
		#check if it is a template class:
		if stack[0] == "template":
			debug.debug("find a template class: " + str(stack))
			#remove template properties ==> not manage for now ...
			stack = stack[stack.index("class"):]
			# TODO : add the template properties back ...
		if len(stack) < 2:
			debug.error("Can not parse class 2 : " + str(stack))
			return
		Node.Node.__init__(self, 'class', stack[1], file, lineNumber, documentation)
		self.subList = []
		self.access = "private"
		# heritage list :
		self.inherit = []
		if len(stack) == 2:
			# just a simple class...
			return
		if len(stack) == 3:
			debug.error("error in parsing class : " + str(stack))
			return
		if stack[2] != ':':
			debug.error("error in parsing class : " + str(stack) + " missing ':' at the 3rd position ...")
		
		list = concatenate_template(stack[3:])
		debug.verbose("inherit : " + str(list))
		access = "private"
		for element in list:
			if element in ['private', 'protected', 'public']:
				access = element
			elif element == ',':
				pass
			else:
				self.inherit.append({'access' : access, 'class' : element})
		
		debug.verbose("class : " + self.to_str())
	
	def to_str(self) :
		ret = "class " + self.name
		if len(self.inherit) != 0 :
			ret += " : "
			isFirst = True
			for element in self.inherit:
				if isFirst == False:
					ret += ", "
				isFirst = False
				ret += element['access'] + " " + element['class']
		ret += " { ... };"
		return ret
	
	def get_parents(self):
		if len(self.inherit) == 0:
			return []
		# note this ony get the first parent ...
		parent = module.get_element_with_name(self.inherit[0]['class'])
		cparent = []
		if parent != None:
			#debug.info(" plop : " + self.name + " " + str(parent) + " " + parent.get_name())
			cparent = parent.get_parents()
			pass
		#heritage = parent.
		cparent.append(self.inherit[0])
		return cparent
	
	def get_whith_specific_parrent(self, parrentName):
		ret = []
		for parrent in self.inherit:
			if parrentName == self.inherit[0]['class']:
				ret.append(self.get_displayable_name())
		# set for all sub elements ...
		if self.subList != None:
			for element in self.subList:
				tmpRet = element['node'].get_whith_specific_parrent(parrentName)
				if len(tmpRet) != 0:
					for tmp in tmpRet:
						ret.append(tmp)
		return ret


