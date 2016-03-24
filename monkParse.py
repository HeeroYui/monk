#!/usr/bin/python
import os
import sys
import re

import monkTools as tools

sys.path.append(tools.get_current_path(__file__) + "/ply/ply/")
sys.path.append(tools.get_current_path(__file__) + "/codeBB/")
sys.path.append(tools.get_current_path(__file__) + "/codeHL/")

import lex

import inspect
import monkDebug as debug
import monkClass as Class
import monkNamespace as Namespace
import monkStruct as Struct
import monkUnion as Union
import monkMethode as Methode
import monkEnum as Enum
import monkVariable as Variable
import monkNode as Node

tokens = [
	'NUMBER',
	'TEMPLATE',
	'NAME',
	'OPEN_PAREN',
	'CLOSE_PAREN',
	'OPEN_BRACE',
	'CLOSE_BRACE',
	'OPEN_SQUARE_BRACKET',
	'CLOSE_SQUARE_BRACKET',
	'COLON',
	'SEMI_COLON',
	'COMMA',
	'TAB',
	'BACKSLASH',
	'PIPE',
	'PERCENT',
	'EXCLAMATION',
	'CARET',
	'COMMENT_SINGLELINE_DOC_PREVIOUS',
	'COMMENT_SINGLELINE_DOC',
	'COMMENT_SINGLELINE',
	'COMMENT_MULTILINE_DOC',
	'COMMENT_MULTILINE',
	'PRECOMP',
	'ASTERISK',
	'AMPERSTAND',
	'EQUALS',
	'MINUS',
	'PLUS',
	'DIVIDE',
	'CHAR_LITERAL',
	'STRING_LITERAL',
	'NEW_LINE',
	'SQUOTE',
]

t_ignore = " \r.?@\f"
t_TEMPLATE = r'template'
t_NUMBER = r'[0-9][0-9XxA-Fa-f]*L?'
t_NAME = r'[<>A-Za-z_~][A-Za-z0-9_]*'
t_OPEN_PAREN = r'\('
t_CLOSE_PAREN = r'\)'
t_OPEN_BRACE = r'{'
t_CLOSE_BRACE = r'}'
t_OPEN_SQUARE_BRACKET = r'\['
t_CLOSE_SQUARE_BRACKET = r'\]'
t_SEMI_COLON = r';'
t_COLON = r':'
t_COMMA = r','
def t_TAB(t):
	r'\t'
t_BACKSLASH = r'\\'
t_PIPE = r'\|'
t_PERCENT = r'%'
t_CARET = r'\^'
t_EXCLAMATION = r'!'
def t_PRECOMP(t):
	r'\#.*?\n'
	t.value = re.sub(r'\#\#multiline\#\#', "\\\n", t.value)
	t.lexer.lineno += len(filter(lambda a: a=="\n", t.value))
	return t
def t_COMMENT_SINGLELINE_DOC_PREVIOUS(t):
	r'//(/|!)<.*?\n'
	t.lexer.lineno += 1
	t.value = t.value[4:]
	while t.value[0] in ['\n', '\t', ' ']:
		if len(t.value) <= 2:
			break
		t.value = t.value[1:]
	while t.value[-1] in ['\n', '\t', ' ']:
		if len(t.value) <= 2:
			break
		t.value = t.value[:-1]
	return t
def t_COMMENT_SINGLELINE_DOC(t):
	r'//(/|!).*?\n'
	t.lexer.lineno += 1
	t.value = t.value[3:]
	while t.value[0] in ['\n', '\t', ' ']:
		if len(t.value) <= 2:
			break
		t.value = t.value[1:]
	while t.value[-1] in ['\n', '\t', ' ']:
		if len(t.value) <= 2:
			break
		t.value = t.value[:-1]
	return t
def t_COMMENT_SINGLELINE(t):
	r'\/\/.*\n'
	t.lexer.lineno += 1
t_ASTERISK = r'\*'
t_MINUS = r'\-'
t_PLUS = r'\+'
t_DIVIDE = r'/(?!/)'
t_AMPERSTAND = r'&'
t_EQUALS = r'='
t_CHAR_LITERAL = "'.'"
t_SQUOTE = "'"
#found at http://wordaligned.org/articles/string-literals-and-regular-expressions
#TODO: This does not work with the string "bla \" bla"
t_STRING_LITERAL = r'"([^"\\]|\\.)*"'
#Found at http://ostermiller.org/findcomment.html
def t_COMMENT_MULTILINE_DOC(t):
	r'/\*(\*|!)(\n|.)*?\*/'
	t.lexer.lineno += len(filter(lambda a: a=="\n", t.value))
	t.value = re.sub("( |\t)*\*", "", t.value[3:-2])
	while t.value[0] == '\n':
		if len(t.value) <= 2:
			break
		t.value = t.value[1:]
	while t.value[-1] in ['\n', '\t', ' ']:
		if len(t.value) <= 2:
			break
		t.value = t.value[:-1]
	removeLen = 9999
	
	listElement = t.value.split('\n')
	for line in listElement:
		tmpLen = 0
		for element in line:
			if element == ' ':
				tmpLen += 1
			else:
				break;
		if removeLen > tmpLen:
			removeLen = tmpLen
	if removeLen == 9999:
		return t
	ret = ""
	isFirst = True
	for line in listElement:
		if isFirst == False:
			ret += '\n'
		isFirst = False
		ret += line[removeLen:]
	t.value = ret
	return t
def t_COMMENT_MULTILINE(t):
	r'/\*(\n|.)*?\*/'
	t.lexer.lineno += len(filter(lambda a: a=="\n", t.value))
def t_NEWLINE(t):
	r'\n+'
	t.lexer.lineno += len(t.value)

def t_error(v):
	print( "Lex error: ", v )

lex.lex()

##
## @brief Join the class name element : ['class', 'Bar', ':', ':', 'Foo'] -> ['class', 'Bar::Foo']
## @param table Input table to convert. ex: [':', '\t', 'class', 'Bar', ':', ':', 'Foo']
## @return The new table. ex: ['class', 'Bar::Foo']
##
def create_compleate_class_name(table):
	debug.warning("table = " + str(table))
	if "::" not in "".join(table):
		out = table
	else:
		# we need to convert it :
		out = []
		for name in table:
			if len(out) == 0: 
				out.append(name)
			elif     name == ":" \
			     and out[-1].endswith(":"):
				out[-1] += name
			elif out[-1].endswith("::"):
				out[-2] += out[-1] + name
				del out[-1]
			else:
				out.append(name)
	table = out
	if 'operator' not in "".join(table):
		out = table
	else:
		out = []
		for name in table:
			if len(out) == 0:
				out.append(name)
			elif     out[-1][:8] == 'operator' \
			     and name != '(':
				if out[-1] == 'operator':
					out[-1] += ' '
				if out[-1][-1] not in [' ', '<','>','=', '-', '!', '+', '*', '&', '|', '/']:
					out[-1] += ' '
				out[-1] += name
			else:
				out.append(name)
	debug.warning("    ==> out = " + str(out))
	return out


class parse_file():
	
	def gen_debug_space(self):
		ret = "[" + str(len(self.brace_depth_type)+1) + "]"
		for iii in range(0,len(self.brace_depth_type)):
			ret += "    "
		return ret
	
	def fusion(self, baseNode):
		baseNode.fusion(self.main_node)
		return baseNode
	
	def __init__(self, fileName):
		self.main_node = Node.MainNode("main-node", "tmp")
		self.element_parse_stack = []
		debug.debug("Parse file : '" + fileName + "'")
		
		self.header_file_name = fileName
		
		self.anon_union_counter = [-1, 0]
		# load all the file data :
		headerFileStr = tools.file_read_data(fileName)
		
		# Strip out template declarations
		# TODO : What is the real need ???
		#headerFileStr = re.sub("template[\t ]*<[^>]*>", "", headerFileStr)
		# remove all needed \r unneeded ==> this simplify next resExp ...
		headerFileStr = re.sub("\r", "\r\n", headerFileStr)
		headerFileStr = re.sub("\r\n\n", "\r\n", headerFileStr)
		headerFileStr = re.sub("\r", "", headerFileStr)
		# TODO : Can generate some error ...
		headerFileStr = re.sub("\#if 0(.*?)(\#endif|\#else)", "", headerFileStr, flags=re.DOTALL)
		headerFileafter = re.sub("\@interface(.*?)\@end", "", headerFileStr, flags=re.DOTALL)
		if headerFileStr != headerFileafter :
			debug.debug(" Objective C interface ... ==> not supported")
			return
		
		#debug.verbose(headerFileStr)
		
		#Filter out Extern "C" statements. These are order dependent
		headerFileStr = re.sub(r'extern( |\t)+"[Cc]"( |\t)*{', "{", headerFileStr)
		headerFileStr = re.sub(r'\\\n', "##multiline##", headerFileStr)
		headerFileStr += '\n'
		debug.debug(headerFileStr)
		
		###### debug.info(headerFileStr)
		self.stack = [] # token stack to find the namespace and the element name ...
		self.previous = None
		self.name_stack = [] # 
		self.brace_depth = 0
		self.brace_depth_type = []
		self.last_comment = []
		self.sub_module_count_brace = 0;
		lex.lex()
		lex.input(headerFileStr)
		self.cur_line = 0
		self.cur_char = 0
		while True:
			tok = lex.token()
			if not tok:
				break
			debug.verbose("TOK: " + str(tok))
			self.stack.append( tok.value )
			self.cur_line = tok.lineno
			self.cur_char = tok.lexpos
			# special case to remove internal function define in header:
			if self.previous_is('function') == True:
				if tok.type == 'OPEN_BRACE':
					self.sub_module_count_brace += 1
					debug.verbose("openBrace " + str(self.sub_module_count_brace))
				elif tok.type == 'CLOSE_BRACE':
					self.sub_module_count_brace -= 1
					debug.verbose("closeBrace " + str(self.sub_module_count_brace) + " line:" + str(self.cur_line))
				if self.sub_module_count_brace <= 0:
					self.brace_type_pop()
					self.last_comment = []
				continue
			# normal case:
			if tok.type == 'PRECOMP':
				debug.debug("PRECOMP: " + str(tok))
				self.stack = []
				self.name_stack = []
				self.last_comment = []
				# Do nothing for macro ==> many time not needed ...
				continue
			if tok.type == 'COMMENT_SINGLELINE_DOC_PREVIOUS':
				if self.previous_is('enum') == True:
					if self.name_stack[-1] == ",":
						self.name_stack[-1] = "//!< " + tok.value
						self.name_stack.append(",")
					else:
						self.name_stack.append("//!< " + tok.value)
				elif     self.previous != None \
				     and self.previous.get_node_type() == 'variable':
					self.previous.add_doc([tok.value])
				else:
					#self.last_comment.append(tok.value)
					pass
			if tok.type == 'COMMENT_MULTILINE_DOC':
				self.last_comment.append(tok.value)
			if tok.type == 'COMMENT_SINGLELINE_DOC':
				self.last_comment.append(tok.value)
			if tok.type == 'OPEN_BRACE':
				# When we open a brace, this is the time to parse the stack ...
				# Clean the stack : (remove \t\r\n , and concatenate the 'xx', ':', ':', 'yy'  in 'xx::yy',
				self.name_stack = create_compleate_class_name(self.name_stack)
				if len(self.name_stack) <= 0:
					#open brace with no name ...
					self.brace_type_push('empty', [])
				elif is_a_function(self.name_stack):
					# need to parse sub function internal description...
					self.sub_module_count_brace = 1
					self.brace_type_push('function', self.name_stack)
					debug.verbose("openBrace *** " + str(self.name_stack))
				elif 'namespace' in self.name_stack:
					self.brace_type_push('namespace', self.name_stack)
				elif 'class' in self.name_stack:
					self.brace_type_push('class', self.name_stack)
				elif 'enum' in self.name_stack:
					self.brace_type_push('enum', self.name_stack)
				elif 'struct' in self.name_stack:
					self.brace_type_push('struct', self.name_stack)
				elif 'typedef' in self.name_stack:
					self.brace_type_push('typedef', self.name_stack)
				elif 'union' in self.name_stack:
					self.brace_type_push('union', self.name_stack)
				else:
					self.brace_type_push('unknow', self.name_stack)
				self.stack = []
				self.name_stack = []
				self.last_comment = []
			elif tok.type == 'CLOSE_BRACE':
				if len(self.name_stack) != 0:
					if self.previous_is('enum') == True:
						self.brace_type_append('enum list', self.name_stack);
					else:
						debug.warning(self.gen_debug_space() + "end brace DROP : " + str(self.name_stack));
				self.stack = []
				self.name_stack = []
				self.last_comment = []
				self.brace_type_pop()
				self.name_stack = create_compleate_class_name(self.name_stack)
			if tok.type == 'OPEN_PAREN':
				self.name_stack.append(tok.value)
			elif tok.type == 'CLOSE_PAREN':
				self.name_stack.append(tok.value)
			elif tok.type == 'OPEN_SQUARE_BRACKET':
				self.name_stack.append(tok.value)
			elif tok.type == 'CLOSE_SQUARE_BRACKET':
				self.name_stack.append(tok.value)
			elif tok.type == 'EQUALS':
				self.name_stack.append(tok.value)
			elif tok.type == 'COMMA':
				self.name_stack.append(tok.value)
			elif tok.type == 'BACKSLASH':
				self.name_stack.append(tok.value)
			elif tok.type == 'PIPE':
				self.name_stack.append(tok.value)
			elif tok.type == 'PERCENT':
				self.name_stack.append(tok.value)
			elif tok.type == 'CARET':
				self.name_stack.append(tok.value)
			elif tok.type == 'EXCLAMATION':
				self.name_stack.append(tok.value)
			elif tok.type == 'SQUOTE':
				self.name_stack.append(tok.value)
			elif tok.type == 'NUMBER':
				self.name_stack.append(tok.value)
			elif tok.type == 'MINUS':
				self.name_stack.append(tok.value)
			elif tok.type == 'PLUS':
				self.name_stack.append(tok.value)
			elif tok.type == 'STRING_LITERAL':
				self.name_stack.append(tok.value)
			elif     tok.type == 'NAME' \
			      or tok.type == 'AMPERSTAND' \
			      or tok.type == 'ASTERISK' \
			      or tok.type == 'CHAR_LITERAL':
				self.name_stack.append(tok.value)
			elif tok.type == 'COLON':
				if self.name_stack[0] in Node.accessList:
					debug.debug(self.gen_debug_space() + "change visibility : " + self.name_stack[0]);
					self.brace_type_change_access(self.name_stack[0])
					self.name_stack = []
					self.stack = []
				else :
					self.name_stack.append(tok.value)
			elif tok.type == 'SEMI_COLON':
				if len(self.name_stack) != 0:
					self.name_stack = create_compleate_class_name(self.name_stack)
					if is_a_function(self.name_stack):
						self.brace_type_append('function', self.name_stack);
					elif 'namespace' in self.name_stack:
						debug.debug(self.gen_debug_space() + "find a namespace DECLARATION : " + str(self.name_stack));
					elif 'class' in self.name_stack:
						debug.debug(self.gen_debug_space() + "find a class     DECLARATION : " + str(self.name_stack));
					elif 'enum' in self.name_stack:
						debug.debug(self.gen_debug_space() + "find a enum      DECLARATION : " + str(self.name_stack));
					elif 'struct' in self.name_stack:
						debug.debug(self.gen_debug_space() + "find a struct    DECLARATION : " + str(self.name_stack));
					elif 'typedef' in self.name_stack:
						debug.info(self.gen_debug_space() + "find a typedef   DECLARATION : " + str(self.name_stack));
					elif 'union' in self.name_stack:
						debug.debug(self.gen_debug_space() + "find a union     DECLARATION : " + str(self.name_stack));
					else:
						if self.previous_is('enum') == True:
							self.brace_type_append('enum list', self.name_stack);
						else:
							# TODO : Check if it is true in all case : 
							self.brace_type_append('variable', self.name_stack);
							#debug.warning(self.gen_debug_space() + "variable : " + str(self.name_stack));
				self.stack = []
				self.name_stack = []
				self.last_comment = []
		#self.debug_display();
	
	def debug_display(self):
		debug.info("Debug display :")
		self.main_node.debug_display(1)
	
	def create_element(self, type, stack):
		ret = None
		self.previous = None
		if    type == 'empty' \
		   or type == 'enum list':
			pass
		elif type == 'namespace':
			ret = Namespace.Namespace(stack, self.header_file_name, self.cur_line, self.last_comment)
		elif type == 'class':
			ret = Class.Class(stack, self.header_file_name, self.cur_line, self.last_comment)
		elif type == 'struct':
			ret = Struct.Struct(stack, self.header_file_name, self.cur_line, self.last_comment)
		elif type == 'typedef':
			#ret = Namespace.Namespace(stack, self.header_file_name, self.cur_line)
			# TODO ...
			pass
		elif type == 'union':
			ret = Union.Union(stack, self.header_file_name, self.cur_line, self.last_comment)
		elif type == 'function':
			#debug.info(str(self.last_comment))
			if self.get_last_type() == 'class':
				ret = Methode.Methode(stack, self.header_file_name, self.cur_line, self.last_comment, self.brace_depth_type[len(self.brace_depth_type)-1]['node'].get_name())
			else:
				ret = Methode.Methode(stack, self.header_file_name, self.cur_line, self.last_comment)
		elif type == 'enum':
			ret = Enum.Enum(stack, self.header_file_name, self.cur_line, self.last_comment)
		elif type == 'variable':
			ret = Variable.Variable(stack, self.header_file_name, self.cur_line, self.last_comment)
			self.previous = ret
		else:
			debug.error("unknow type ...")
		return ret
	
	def brace_type_push(self, type, stack):
		debug.debug(self.gen_debug_space() + "find a <<" + type + ">> : " + str(stack));
		myClassElement = self.create_element(type, stack)
		element = { 'type' : type,
		            'stack' : stack,
		            'node' : myClassElement
		          }
		self.brace_depth_type.append(element)
		#debug.info ("append : " + str(element))
	
	def brace_type_append_current(self, element, id = -50):
		if id == -50:
			id = len(self.brace_depth_type)-1
		if id >= 0:
			while self.brace_depth_type[id]['node'] == None:
				# special case for empty brace, just add it to the upper
				id -=1
				if id < 0:
					break;
		if id < 0:
			self.main_node.append(element)
		else:
			self.brace_depth_type[id]['node'].append(element)
	
	def brace_type_append(self, type, stack):
		debug.debug(self.gen_debug_space() + " append a <<" + type + ">> : " + str(stack));
		lastType = self.get_last_type()
		newType = self.create_element(type, stack)
		if newType != None:
			self.brace_type_append_current(newType)
			return
		# enum sub list:
		if     lastType == 'enum' \
		   and type == 'enum list':
			id = len(self.brace_depth_type)-1
			self.brace_depth_type[id]['node'].enum_append(stack)
			return
		debug.info("TODO : Parse the special type")
	
	def brace_type_pop(self):
		id = len(self.brace_depth_type)-1
		if id < 0:
			debug.warning("Try to pop the stack with No more element ...")
			return
		if self.brace_depth_type[id]['node'] == None:
			# nothing to add at the upper ...
			pass
		else:
			# add it on the previous
			self.brace_type_append_current(self.brace_depth_type[id]['node'], id-1)
		self.brace_depth_type.pop()
	
	def brace_type_change_access(self, newOne):
		if newOne not in Node.accessList:
			debug.error("unknow access type : " + newOne)
			return
		id = len(self.brace_depth_type)-1
		if id >= 0:
			while self.brace_depth_type[id]['node'] == None:
				# special case for empty brace, just add it to the upper
				id -=1
				if id < 0:
					break;
		if id < 0:
			debug.warning("can not change the main access on the library")
		else:
			if self.brace_depth_type[id]['node'].get_access() == None:
				debug.error("Can not set access in other as : 'class' or 'struct' :" + str(self.brace_depth_type[id]))
				return
			self.brace_depth_type[id]['node'].set_access(newOne)
	
	def previous_is(self, type):
		if self.get_last_type() == type:
			return True
		return False
	
	def get_last_type(self):
		if len(self.brace_depth_type) > 0:
			return self.brace_depth_type[len(self.brace_depth_type)-1]['type']
		return None

def is_a_function(stack) :
	# in a function we need to have functionName + ( + )
	if len(stack) < 3:
		return False
	if ':' in stack:
		res = []
		for element in stack:
			if element != ':':
				res.append(element)
			else:
				break
		stack = res
	if     stack[len(stack)-2] == '=' \
	   and stack[len(stack)-1] == '0':
		stack = stack[:len(stack)-2]
	# find ')' element :
	id = len(stack)-1
	while id >= 0:
		if stack[id] == ')':
			break;
		id -= 1
	if id >= 0:
		for elem in stack[id+1:]:
			if elem not in ['const', 'noexcept', 'override']:
				return False
		return True
	return False