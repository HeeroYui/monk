#!/usr/bin/python
import monkDebug as debug
import monkNode as Node

class Typedef(Node.Node):
	def __init__(self, stack=[], file="", lineNumber=0, documentation=[]):
		name = ""
		debug.warning(" typedef : " + str(stack))
		Node.Node.__init__(self, 'typedef', name, file, lineNumber, documentation)
		
	
	def to_str(self) :
		return "typedef " + self.name + " { ... };"
		

