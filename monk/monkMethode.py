##!/usr/bin/python
from realog import debug
import monkNode as Node
import monkType as Type
import monkVariable as Variable

class Methode(Node.Node):
	def __init__(self, stack=[], file="", lineNumber=0, documentation=[], className = ""):
		name = ""
		type = 'methode'
		self.override = False
		self.virtual = False
		self.virtual_pure = False
		self.static = False
		self.inline = False
		self.const = False # the end of line cont methode is sont for the class ...
		self.noexcept = False
		self.override = False
		self.delete = False
		
		# remove constructer inside declaration ...
		if ':' in stack:
			res = []
			for element in stack:
				if element != ':':
					res.append(element)
				else:
					break
			stack = res
		
		#check if it is a template methode:
		# note: A methode template can contain multiple methode handle ...
		while stack[0] == "template":
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
			self.virtual_pure = True
		
		if     stack[len(stack)-2] == '=' \
		   and stack[len(stack)-1] == 'delete':
			stack = stack[:len(stack)-2]
			self.delete = True
		
		while len(stack) > 0\
		      and (    stack[0] == 'virtual'\
		            or stack[0] == 'static'\
		            or stack[0] == 'inline')::
			if stack[0] == 'virtual':
				self.virtual = True
				stack = stack[1:]
			if stack[0] == 'static':
				self.static = True
				stack = stack[1:]
			if stack[0] == 'inline':
				self.inline = True
				stack = stack[1:]
		while stack[-1] in ['override', 'noexcept', 'const']:
			if stack[-1] == 'override':
				self.override = True
				stack = stack[:-1]
			if stack[-1] == 'noexcept':
				self.noexcept = True
				stack = stack[:-1]
			if stack[-1] == 'const':
				self.const = True
				stack = stack[:-1]
		
		debug.debug("methode parse : " + str(stack))
		namePos = -1
		# form start to '(' char we will concatenate the name of the function wit template attributes 
		# ex:  ['esignal', '::', 'Signal', '<', 'T_ARGS', '>', '::', 'Signal', '(', 'CLASS_TYPE', '*', '_class', ',', 'FUNC_TYPE', '_func', ')']
		#  ==> ['esignal::Signal<T_ARGS>::Signal', '(', 'CLASS_TYPE', '*', '_class', ',', 'FUNC_TYPE', '_func', ')']
		# find pos of '(':
		namePos = len(stack)
		namePosStart = 0
		for iii in range(0, len(stack)):
			if stack[iii] == '(':
				namePos = iii
				break;
			if     iii != 0 \
			   and not (    stack[iii-1] in ["::", "<", ">", ","]
			             or stack[iii] in ["::", "<", ">", ","]) :
				namePosStart = iii
		if namePos == len(stack):
			debug.error(" can not parse function name :" + str(stack))
		name = "".join(stack[namePosStart: namePos])
		if namePosStart == 0:
			debug.verbose("start with '" + str(name[0]) + "'")
			if name[0] == '~':
				if className == name[1:]:
					type = 'destructor'
			else:
				if className == name:
					type = 'constructor'
		debug.debug("methode name : " + name)
		Node.Node.__init__(self, type, name, file, lineNumber, documentation)
		
		self.return_type = Type.TypeNone()
		self.variable = []
		
		# create the return Type (Can be Empty)
		retTypeStack = stack[:namePosStart]
		debug.debug("return : " + str(retTypeStack))
		self.return_type = Type.Type(retTypeStack)
		
		parameterStack = stack[namePos+1:len(stack)-1]
		debug.debug("parameter : " + str(parameterStack))
		paramTmp = []
		braceOpen = 0
		for element in parameterStack:
			if braceOpen == 0:
				if element == ',':
					self.variable.append(Variable.Variable(paramTmp))
					paramTmp = []
				elif element in ['(', '<']:
					paramTmp.append(element)
					braceOpen += 1
				else:
					paramTmp.append(element)
			else:
				paramTmp.append(element)
				if element in ['(', '<']:
					braceOpen += 1
				elif element in [')', '>']:
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
		raw, decorated = self.return_type.to_str_decorated()
		ret += raw
		retDecorated += decorated
		ret += " "
		ret += self.name
		ret += "("
		# ...
		ret += ")"
		if self.virtual_pure == True:
			ret += " = 0"
			retDecorated += " = 0"
		if self.const == True:
			ret += " const"
			retDecorated += " " + module.display_color("const")
		if self.noexcept == True:
			ret += " noexcept"
			retDecorated += " " + module.display_color("noexcept")
		if self.override == True:
			ret += " override"
			retDecorated += " " + module.display_color("override")
		if self.delete == True:
			ret += " = delete"
			retDecorated += " = " + module.display_color("delete")
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
		return self.virtual_pure
	
	##
	## @brief Get the status of the delete function ( virtual XXX(...) = delete;)
	## @return True if =delete is present, False otherwise
	##
	def get_delete(self):
		return self.delete
	
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
		return self.return_type
	
	##
	## @brief Get the list of parameter of the methode
	## @return The requested list of parameter
	##
	def get_param(self):
		return self.variable
	##
	## @brief Get Override parameter
	## @return The requested override parameter
	##
	def get_override(self):
		return self.override


