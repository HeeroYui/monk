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
	"std::shared_ptr": "http://www.cplusplus.com/reference/memory/shared_ptr/",
	"std::weak_ptr"  : "http://www.cplusplus.com/reference/memory/weak_ptr/",
	"std::enable_shared_from_this" : "http://www.cplusplus.com/reference/memory/enable_shared_from_this/"
	}


class Type():
	def __init__(self, stack=[]):
		self.nameBefore = ""
		self.name = ""
		self.nameAfter = ""
		self.const = False # the const xxxxx
		self.reference = False
		self.constVar = False # the char* const VarName
		self.enum = False
		self.struct = False
		
		if len(stack) == 0:
			# None type
			return
		if len(stack) == 1:
			self.name = stack[0]
			return;
		# check end const
		if stack[len(stack)-1] == 'const':
			self.constVar = True
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
		
		self.nameBefore = ""
		self.name = ""
		self.nameAfter = ""
		for element in stack:
			if self.nameAfter != "":
				self.nameAfter += element
				continue
			if element[0] in ['*', '&', '<']:
				if self.name == "":
					self.nameBefore += element
					continue
				else:
					self.nameAfter += element
					continue
			self.name += element
		#debug.info("get type : " + str(stack) + " ==> " +self.name)
	
	def to_str(self) :
		ret = ""
		if self.const == True:
			ret += "const "
		if self.enum == True:
			ret += "enum "
		if self.struct == True:
			ret += "struct "
			
		ret += self.nameBefore
		ret += self.name
		ret += self.nameAfter
		if self.reference == True:
			ret += " &"
		if self.constVar == True:
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
		if self.enum == True:
			ret += "enum "
			retDecorated += module.display_color("enum") + " "
		if self.struct == True:
			ret += "struct "
			retDecorated += module.display_color("struct") + " "
		ret += self.nameBefore
		ret += self.name
		ret += self.nameAfter
		retDecorated += self.nameBefore
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
		retDecorated += re.sub(">","&gt;", re.sub("<","&lt;", self.nameAfter))
		if self.reference == True:
			ret          += " &"
			retDecorated += " &"
		if self.constVar == True:
			ret          += " const"
			retDecorated += " " + module.display_color("const")
		return [ret, retDecorated]

class TypeVoid(Type):
	def __init__(self):
		Type.__init__(self, ['void'])

class TypeNone(Type):
	def __init__(self):
		Type.__init__(self)

