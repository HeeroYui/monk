#!/usr/bin/python
import monkDebug as debug
import monkNode as Node

class Namespace(Node.Node):
	def __init__(self, stack=[], file="", lineNumber=0, documentation=[]):
		if len(stack) != 2:
			debug.error("Can not parse namespace : " + str(stack))
		Node.Node.__init__(self, 'namespace', stack[1], file, lineNumber, documentation)
		# enable sub list
		self.sub_list = []
		
		debug.verbose("find namespace : " + self.to_str())
	
	def to_str(self) :
		return "namespace " + self.name + " { ... };"
		

