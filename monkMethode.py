##!/usr/bin/python
import monkDebug as debug
import monkNode as Node
import monkType as Type
import monkVariable as Variable

class Methode(Node.Node):
	def __init__(self, stack=[], file="", lineNumber=0, documentation=[], className = ""):
		name = ""
		type = 'methode'
		self.virtual = False
		self.virtualPure = False
		self.static = False
		self.inline = False
		self.const = False # the end of line cont methode is sont for the class ...
		self.noexcept = False
		
		# remove constructer inside declaration ...
		if ':' in stack:
			res = []
			for element in stack:
				if element != ':':
					res.append(element)
				else:
					break
			stack = res
		
		#check if it is a template class:
		if stack[0] == "template":
			debug.debug("find a template methode: " + str(stack))
			#remove template properties ==> not manage for now ...
			newStack = []
			counter = 0
			counterEnable = True
			# start at the first '<'
			for element in stack[1:]:
				if counterEnable == True:
					if element[0] == '<':
						counter += 1;
					elif element[0] == '>':
						counter -= 1;
				if counter == 0:
					if counterEnable == True:
						counterEnable = False
					else:
						newStack.append(element)
			stack = newStack
			# TODO : add the template properties back ...
			debug.verbose("find a template methode: " + str(stack))
		
		if     stack[len(stack)-2] == '=' \
		   and stack[len(stack)-1] == '0':
			stack = stack[:len(stack)-2]
			self.virtualPure = True
		
		if stack[0] == 'virtual':
			self.virtual = True
			stack = stack[1:]
		if stack[0] == 'static':
			self.static = True
			stack = stack[1:]
		if stack[0] == 'inline':
			self.inline = True
			stack = stack[1:]
		if stack[len(stack)-1] == 'noexcept':
			self.noexcept = True
			stack = stack[:len(stack)-1]
		if stack[len(stack)-1] == 'const':
			self.const = True
			stack = stack[:len(stack)-1]
		
		namePos = -1
		
		debug.debug("methode parse : " + str(stack))
		for iii in range(0, len(stack)-2):
			if stack[iii+1] == '(':
				name = stack[iii]
				namePos = iii
				break;
		
		if namePos == 0:
			debug.debug("start with '" + str(name[0]) + "'")
			if name[0] == '~':
				if className == name[1:]:
					type = 'destructor'
			else:
				if className == name:
					type = 'constructor'
		debug.debug("methode name : " + name)
		Node.Node.__init__(self, type, name, file, lineNumber, documentation)
		
		self.returnType = Type.TypeNone()
		self.variable = []
		
		# create the return Type (Can be Empty)
		retTypeStack = stack[:namePos]
		debug.debug("return : " + str(retTypeStack))
		self.returnType = Type.Type(retTypeStack)
		
		parameterStack = stack[namePos+2:len(stack)-1]
		debug.debug("parameter : " + str(parameterStack))
		paramTmp = []
		braceOpen = 0
		for element in parameterStack:
			if braceOpen == 0:
				if element == ',':
					self.variable.append(Variable.Variable(paramTmp))
					paramTmp = []
				elif element == '(':
					paramTmp.append(element)
					braceOpen += 1
				else:
					paramTmp.append(element)
			else:
				paramTmp.append(element)
				if element == '(':
					braceOpen += 1
				elif element == ')':
					braceOpen -= 1
		if len(paramTmp) != 0:
			self.variable.append(Variable.Variable(paramTmp))
	
	def to_str(self):
		return self.to_str_decorated()[0]
	
	def to_str_decorated(self):
		ret = ""
		retDecorated = ""
		if self.virtual == True:
			ret          += "virtual "
			retDecorated += module.display_color("virtual") + " "
		if self.static == True:
			ret += "static "
			retDecorated += module.display_color("static") + " "
		if self.inline == True:
			ret += "inline "
			retDecorated += module.display_color("inline") + " "
		raw, decorated = self.returnType.to_str_decorated()
		ret += raw
		retDecorated += decorated
		ret += " "
		ret += self.name
		ret += "("
		# ...
		ret += ")"
		if self.virtualPure == True:
			ret += " = 0"
			retDecorated += " = 0"
		if self.const == True:
			ret += " const"
			retDecorated += " " + module.display_color("const")
		if self.noexcept == True:
			ret += " noexcept"
			retDecorated += " " + module.display_color("noexcept")
		return [ret, retDecorated]
	
	##
	## @brief Get the status of the virtual function ( virtual XXX(...);)
	## @return True if vitual is present, False otherwise
	## @note This is only availlable for class methode
	##
	def get_virtual(self):
		return self.virtual
	
	##
	## @brief Get the status of the virtual 'pure' function ( virtual XXX(...) = 0;)
	## @return True if =0 is present, False otherwise
	## @note This is only availlable for class methode
	## @note Availlable only if the virtual is active
	##
	def get_virtual_pure(self):
		return self.virtualPure
	
	##
	## @brief Get the status of the inline function ( inline XXX(...);)
	## @return True if inline is present, False otherwise
	##
	def get_inline(self):
		return self.inline
	
	##
	## @brief Get the status of the static function ( static XXX(...);)
	## @return True if static is present, False otherwise
	## @note This is only availlable for class methode
	##
	def get_static(self):
		return self.static
	
	##
	## @brief Get the status of the constant function ( XXX(...) const;)
	## @return True if const is present, False otherwise
	## @note This is only availlable for class methode
	##
	def get_constant(self):
		return self.const
	
	##
	## @brief Get the return type of the methode
	## @return Return methode type (type: Type.Type)
	##
	def get_return_type(self):
		return self.returnType
	
	##
	## @brief Get the list of parameter of the methode
	## @return The requested list of parameter
	##
	def get_param(self):
		return self.variable


