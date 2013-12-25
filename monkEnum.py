#!/usr/bin/python
import monkDebug as debug
import monkNode as Node

class Enum(Node.Node):
	def __init__(self, stack=[], file="", lineNumber=0, documentation=[]):
		self.baseValue = 0;
		# check input :
		if len(stack) < 2:
			debug.error("Can not parse class : " + str(stack))
			return
		self.typedef = False
		if stack[0] == 'typedef':
			self.typedef = True
			stack[1:]
		
		Node.Node.__init__(self, 'enum', stack[1], file, lineNumber, documentation)
		
		self.listElement = []
	
	def to_str(self) :
		return "enum " + self.name + " { ... };"
	
	def enum_append(self, stack):
		subList = []
		tmp = []
		for element in stack:
			if element == ',':
				subList.append(tmp)
				tmp = []
			else:
				tmp.append(element)
		if len(tmp) != 0:
			subList.append(tmp)
		
		#debug.verbose(" TODO : Need to append enum : " + str(subList))
		for element in subList:
			value = ""
			if len(element) > 2:
				if element[1] == '=':
					for tmp in element[2:]:
						value = tmp
			if value == "":
				if self.baseValue == None:
					value = "???"
				else:
					value = str(self.baseValue)
					self.baseValue += 1
			else:
				try:
					tmpVal = int(value)
					self.baseValue = tmpVal + 1
				except:
					debug.debug("can not parse enum value : '" + value + "'")
					self.baseValue = None
			self.listElement.append({'name' : element[0], 'value' : value, 'doc' : ""})
		
		debug.verbose("enum list : " + str(self.listElement))
	
	def get_enum_list(self):
		return self.listElement


