#!/usr/bin/python
from realog import debug
from . import monkNode as Node

class Union(Node.Node):
	def __init__(self, stack=[], file="", lineNumber=0, documentation=[]):
		name = ""
		Node.Node.__init__(self, 'union', name, file, lineNumber, documentation)
		self.list = []
	
	def to_str(self) :
		return "union " + self.name + " { ... };"
		

