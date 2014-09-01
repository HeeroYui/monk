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

def splitList(list):
	base = []
	out = []
	for elem in list:
		if elem == ",":
			out.append(base)
			base = []
		else:
			base.append(elem)
	if len(base) != 0:
		out.append(base)
		base = []
	return out


class Class(Node.Node):
	def __init__(self, stack=[], file="", lineNumber=0, documentation=[]):
		# check input :
		if len(stack) < 2:
			debug.error("Can not parse class : " + str(stack))
			return
		#check if it is a template class:
		templateDeclatation = []
		if stack[0] == "template":
			debug.debug("find a template class: " + str(stack))
			#remove template properties ==> not manage for now ...
			idEnd = 2
			level = 1
			for tmpClassElem in stack[2:]:
				if tmpClassElem[0] == '<':
					level+=1
				elif tmpClassElem[0] == '>':
					level-=1
					if level == 0:
						break
				idEnd+=1
			propertyTemplate = stack[1:idEnd]
			propertyTemplate[0] = propertyTemplate[0][1:]
			templateDeclatation = splitList(propertyTemplate)
			stack = stack[idEnd+1:]
			# TODO : add the template properties back ...
			debug.debug("template property : " + str(templateDeclatation))
		if len(stack) < 2:
			debug.error("Can not parse class 2 : " + str(stack))
			return
		Node.Node.__init__(self, 'class', stack[1], file, lineNumber, documentation)
		self.template = templateDeclatation
		self.subList = []
		self.access = "private"
		# heritage list :
		self.templateType = None
		self.templateTypeStr = ""
		self.inherit = []
		if len(stack) == 2:
			# just a simple class...
			return
		# remove template specification:
		if stack[2][0] == '<':
			# This is a template
			for iii in range(0, len(stack)):
				if stack[iii] == '>':
					self.templateType = stack[2:iii]
					stack = stack[:2] + stack[iii+1:]
					break;
			# TODO : add tpe in rendering
			if self.templateType == None:
				debug.error("error in parsing class : " + str(stack) + " can not parse template property ...")
			else:
				copyTemplateType = self.templateType;
				self.templateType = []
				self.templateTypeStr = "<"
				for val in copyTemplateType:
					if val[0] == '<':
						val = val[1:]
					if val != '>':
						self.templateType.append(val)
						self.templateTypeStr += val + " "
				self.templateTypeStr = ">"
		if len(stack) == 3:
			debug.error("error in parsing class : " + str(stack))
			return
		if stack[2] != ':':
			debug.error("error in parsing class : " + str(stack) + " missing ':' at the 3rd position ...")
		
		list = concatenate_template(stack[3:])
		debug.verbose("inherit : " + str(list))
		access = "private"
		classProperty = []
		for element in list:
			if element in ['private', 'protected', 'public']:
				access = element
			elif element == ',':
				concatenate = ""
				for classProp in classProperty:
					concatenate += classProp
				self.inherit.append({'access' : access, 'class' : concatenate})
				classProperty = []
			else:
				classProperty.append(element)
		if len(classProperty) != 0:
			concatenate = ""
			for classProp in classProperty:
				concatenate += classProp
			self.inherit.append({'access' : access, 'class' : concatenate})
			classProperty = []
		
		debug.verbose("class : " + self.to_str())
	
	def to_str(self) :
		ret = "class " + self.name
		ret += self.templateTypeStr
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
			debug.verbose("Prent : " + self.name + " " + str(parent) + " " + parent.get_name())
			cparent = parent.get_parents()
			pass
		#heritage = parent.
		cparent.append(self.inherit)
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


