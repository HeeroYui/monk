#!/usr/bin/python
import monkDebug as debug
import monkType as Type
import monkNode as Node

class Variable(Node.Node):
	def __init__(self, stack=[], file="", lineNumber=0, documentation=[]):
		debug.debug("Parse variable : " + str(stack))
		name = ""
		type = []
		if '=' in stack:
			plop = []
			for element in stack:
				if element == "=":
					break
				plop.append(element)
			stack = plop
		
		
		# TODO : better manageement for xxx[**][**] element:
		res = []
		for element in stack:
			if element == '[':
				break
			else:
				res.append(element)
		stack = res
		
		if len(stack) < 2:
			type = stack
		else:
			name = stack[len(stack)-1]
			type = stack[:len(stack)-1]
		
		Node.Node.__init__(self, 'variable', name, file, lineNumber, documentation)
		# force the sublist error  generation ...
		self.sub_list = None
		# default variable :
		self.type = Type.TypeNone()
		self.static = False
		self.external = False
		self.volatile = False
		
		if 'static' in type:
			self.static = True
			type = [value for value in type if value != 'static']
		if 'volatile' in stack:
			self.volatile = True
			type = [value for value in type if value != 'volatile']
		if 'external' in stack:
			self.external = True
			type = [value for value in type if value != 'external']
		
		self.type = Type.Type(type)
		
		debug.verbose("find variable : " + self.to_str())
	
	def to_str(self) :
		ret = ""
		if self.external == True:
			ret += "external "
		if self.volatile == True:
			ret += "volatile "
		if self.static == True:
			ret += "static "
		ret += self.type.to_str()
		ret += " "
		ret += self.name
		return ret
	
	def get_static(self):
		return self.static
	
	def get_volatile(self):
		return self.volatile
	
	def get_external(self):
		return self.external
	
	def get_type(self):
		return self.type
	

