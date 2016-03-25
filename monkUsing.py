#!/usr/bin/python
import monkDebug as debug
import monkNode as Node
import monkType as Type

class Using(Node.Node):
	def __init__(self, stack=[], file="", lineNumber=0, documentation=[]):
		name = stack[1]
		self.access = "public"
		Node.Node.__init__(self, 'using', name, file, lineNumber, documentation)
		self.type = Type.Type(stack[3:])
		debug.verbose(" using : " + str(stack) + " name=" + name + " " + self.type.to_str())
	
	def to_str(self) :
		return "using " + self.name + " { ... };"
	
	def get_type(self):
		return self.type

