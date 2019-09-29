#!/usr/bin/python
from realog import debug
from . import monkNode as Node

class Struct(Node.Node):
	def __init__(self, stack=[], file="", lineNumber=0, documentation=[]):
		name = ""
		Node.Node.__init__(self, 'struct', name, file, lineNumber, documentation)
		self.access = "public"
		self.sub_list = []
		
	
	def to_str(self) :
		return "struct " + self.name + " { ... };"
		

