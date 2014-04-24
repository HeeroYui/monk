#!/usr/bin/python
import monkDebug as debug
import monkNode as Node

class Enum(Node.Node):
	def __init__(self, stack=[], file="", lineNumber=0, documentation=[]):
		self.baseValue = 0;
		# check input :
		if len(stack) < 1:
			debug.error("Can not parse enum : " + str(stack))
			return
		self.typedef = False
		if stack[0] == 'typedef':
			self.typedef = True
			stack[1:]
		if len(stack) == 0:
			debug.error("Can not parse enum : " + str(stack))
			return
		if len(stack) == 1:
			localEnumName = ""
		else:
			localEnumName = stack[1]
		
		Node.Node.__init__(self, 'enum', localEnumName, file, lineNumber, documentation)
		
		self.listElement = []
	
	def to_str(self) :
		return "enum " + self.name + " { ... };"
	
	def enum_append(self, stack):
		debug.verbose("enum : " + str(stack))
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
			# extract comment:
			filtered = []
			comments = ""
			for subs in element:
				if subs[:5] == "//!< ":
					if comments != "":
						comments += "\n"
					comments += subs[5:]
				else:
					filtered.append(subs)
			element = filtered
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
			self.listElement.append({'name' : element[0], 'value' : value, 'doc' : comments})
		
		debug.verbose("enum list : " + str(self.listElement))
	
	def get_enum_list(self):
		return self.listElement


