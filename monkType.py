#!/usr/bin/python
import monkDebug as debug
import monkType as Type
import monkNode as node
import monkModule as module
import re


global_basic_type = ['void', 'bool', \
                     'char', 'char8_t', 'char16_t', 'char32_t', \
                     'float', 'double', \
                     'int', 'unsigned int', 'short', 'unsigned short', 'long', 'unsigned long', \
                     'int8_t',  'int16_t',  'int32_t',  'int64_t',  'int128_t', \
                     'uint8_t', 'uint16_t', 'uint32_t', 'uint64_t', 'uint128_t', \
                     'T', 'CLASS_TYPE']
global_class_link = {
	"std::string"    : "http://www.cplusplus.com/reference/string/string/",
	"std::u16string" : "http://www.cplusplus.com/reference/string/u16string/",
	"std::u32string" : "http://www.cplusplus.com/reference/string/u32string/",
	"std::wstring"   : "http://www.cplusplus.com/reference/string/wstring/",
	"std::vector"    : "http://www.cplusplus.com/reference/vector/vector/",
	"std::list"      : "http://www.cplusplus.com/reference/list/list/",
	"std::pair"      : "http://www.cplusplus.com/reference/utility/pair/",
	"std::tuple"     : "http://www.cplusplus.com/reference/tuple/tuple/",
	"std::ostream"   : "http://www.cplusplus.com/reference/ostream/ostream/",
	"std::shared_ptr": "http://www.cplusplus.com/reference/memory/shared_ptr/",
	"std::weak_ptr"  : "http://www.cplusplus.com/reference/memory/weak_ptr/",
	"std::enable_shared_from_this" : "http://www.cplusplus.com/reference/memory/enable_shared_from_this/"
	}


class Type():
	def __init__(self, stack=[]):
		self.name_before = ""
		self.name = ""
		self.name_after = ""
		self.const = False # the const xxxxx
		self.reference = False
		self.const_var = False # the char* const VarName
		self.enum = False
		self.struct = False
		self.mutable = False
		self.template_parameter = None
		
		if len(stack) == 0:
			# None type
			return
		if len(stack) == 1:
			self.name = stack[0]
			return;
		# check end const
		if stack[len(stack)-1] == 'const':
			self.const_var = True
			stack = stack[:len(stack)-1]
		# check if element is a reference ...
		if stack[len(stack)-1] == '&':
			self.reference = True
			stack = stack[:len(stack)-1]
		# check if it start with const ...
		if stack[0] == 'const':
			self.const = True
			stack = stack[1:]
		# check if it start with enum & struct ...
		if stack[0] == 'enum':
			self.enum = True
			stack = stack[1:]
		if stack[0] == 'struct':
			self.struct = True
			stack = stack[1:]
		if stack[0] == 'mutable':
			self.mutable = True
			stack = stack[1:]
		
		debug.info("get type : " + str(stack))
		self.name_before = ""
		self.name = ""
		self.name_after = ""
		template_level = 0
		template_new_elem = False
		for element in stack:
			if template_level == 0:
				if self.name_after != "":
					self.name_after += element
					continue
				if element[0] in ['*', '&']:
					if self.name == "":
						self.name_before += element
						continue
					else:
						self.name_after += element
						continue
			else:
				if element[0] in [',']:
					#Template separator ...
					template_new_elem = True
					continue
			if element[0] in ['<']:
				debug.info("    Start template")
				if self.template_parameter == None:
					self.template_parameter = []
				if element[1:] != "":
					self.template_parameter.append(element[1:])
				template_level += 1
				continue
			if element[0] in ['>']:
				template_level -= 1
				debug.info("    Stop template")
				continue
			if template_level != 0:
				if element != "":
					if template_new_elem == True:
						self.template_parameter.append(element)
					else:
						self.template_parameter[-1] += " " + element
			else:
				self.name += element
		if self.template_parameter == None:
			debug.info("     ==> '" + self.name + "'")
		else:
			debug.info("     ==> '" + self.name + "'  : " + str(self.template_parameter))
		debug.info("    self.name_before='" + str(self.name_before) + "'")
		debug.info("    self.name_after='" + self.name_after + "'")
	
	def to_str(self) :
		ret = ""
		if self.const == True:
			ret += "const "
		if self.mutable == True:
			ret += "mutable "
		if self.enum == True:
			ret += "enum "
		if self.struct == True:
			ret += "struct "
		ret += self.name_before
		ret += self.name
		if self.template_parameter != None:
			ret += "<"
			first_elem = True
			for elem in self.template_parameter:
				if first_elem == True:
					first_elem = False
				else:
					ret += ", "
				ret += elem
			ret += ">"
		ret += self.name_after
		if self.reference == True:
			ret += " &"
		if self.const_var == True:
			ret += " const"
		return ret
	
	def to_str_decorated(self) :
		global global_basic_type
		global global_class_link
		ret = ""
		retDecorated = ""
		if self.const == True:
			ret          += "const "
			retDecorated += module.display_color("const") + " "
		if self.mutable == True:
			ret          += "mutable "
			retDecorated += module.display_color("mutable") + " "
		if self.enum == True:
			ret += "enum "
			retDecorated += module.display_color("enum") + " "
		if self.struct == True:
			ret += "struct "
			retDecorated += module.display_color("struct") + " "
		ret += self.name_before
		ret += self.name
		ret += self.name_after
		retDecorated += self.name_before
		element = module.get_element_with_name(self.name)
		if element == None:
			
			if self.name in global_basic_type:
				retDecorated += '<span class="code-type" >' + self.name + '</span>'
			elif self.name in global_class_link.keys():
				retDecorated += '<a class="code-type" href="' + global_class_link[self.name] + '">' + self.name + '</a>'
			else:
				retDecorated += self.name
		else:
			currentPageSite = element.get_doc_website_page()
			link = element.get_doc_website_page()
			link = node.get_doc_website_page_relative(currentPageSite, link)
			retDecorated += '<a class="code-type" href="' + link + '">'
			retDecorated += self.name
			retDecorated += '</a>'
		
		if self.template_parameter != None:
			retDecorated += "&lt;"
			ret += "<"
			first_elem = True
			for elem in self.template_parameter:
				if first_elem == True:
					first_elem = False
				else:
					ret += ", "
					retDecorated += ", "
				ret += elem
				retDecorated += elem
			ret += ">"
			retDecorated += "&gt;"
		
		retDecorated += self.name_after
		if self.reference == True:
			ret          += " &"
			retDecorated += " &"
		if self.const_var == True:
			ret          += " const"
			retDecorated += " " + module.display_color("const")
		return [ret, retDecorated]

class TypeVoid(Type):
	def __init__(self):
		Type.__init__(self, ['void'])

class TypeNone(Type):
	def __init__(self):
		Type.__init__(self)

