#!/usr/bin/python
import monkDebug as debug
import monkNode as Node

class Struct(Node.Node):
	def __init__(self, stack=[], file="", lineNumber=0, documentation=[]):
		name = ""
		Node.Node.__init__(self, 'struct', name, file, lineNumber, documentation)
		self.access = "public"
		self.subList = []
		
	
	def to_str(self) :
		return "struct " + self.name + " { ... };"
		

