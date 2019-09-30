#!/usr/bin/python2.7
# for path inspection:
import sys
import os
import inspect
import fnmatch
from . import module
from . import tools
import death.Arguments as arguments
import death.ArgElement as arg_element
from realog import debug


my_args = arguments.Arguments()
my_args.add("h", "help", desc="display this help")
my_args.add_section("option", "Can be set one time in all case")
my_args.add("v", "verbose", haveParam=True, list=[["0","None"],["1","error"],["2","warning"],["3","info"],["4","debug"],["5","verbose"]], desc="Display makefile debug level (verbose) default =2")
my_args.add("C", "color", desc="Display makefile output in color")

my_args.add_section("cible", "generate in order set")
local_argument = my_args.parse()

#debug.set_level(6)

##
## @brief Display the help of this makefile
##
def usage():
	# generic argument displayed : 
	my_args.display()
	print("		all")
	print("			Build all (only for the current selected board) (bynary and packages)")
	print("		clean")
	print("			Clean all (same as previous)")
	listOfAllModule = module.list_all_module_with_desc()
	for mod in listOfAllModule:
		print("		" + mod[0] + " / " + mod[0] + "-clean")
		if mod[1] != "":
			print("			" + mod[1])
	print("	ex: " + sys.argv[0] + " all")
	exit(0)

##
## @brief Preparse the argument to get the verbose element for debug mode
##
def parse_generic_arg(argument,active):
	if argument.get_option_name() == "help":
		#display help
		if active==False:
			usage()
		return True
	elif argument.get_option_name() == "verbose":
		if active==True:
			debug.set_level(int(argument.get_arg()))
		return True
	elif argument.get_option_name() == "color":
		if active==True:
			debug.enable_color()
		return True
	return False

##
## @brief Parse default unique argument:
##
if __name__ == "__main__":
	for argument in local_argument:
		parse_generic_arg(argument, True)

##
## @brief Run everything that is needed in the system
##
def start():
	actionDone=False
	# parse all argument
	for argument in local_argument:
		if parse_generic_arg(argument, False) == True:
			continue
		if argument.get_option_name() != "":
			debug.warning("Can not understand argument : '" + argument.get_option_name() + "'")
			usage()
		else:
			module_value = module.get_module(argument.get_arg())
			module_value.parse_code()
			module_value.generate()
			actionDone=True
	# if no action done : we do "all" ...
	if actionDone==False:
		#Must generate all docs :
		moduleElements = module.get_all_module()
		for module_value in moduleElements:
			module_value.parse_code()
		for module_value in moduleElements:
			module_value.generate()

##
## @brief When the user use with make.py we initialise ourself
##
#if __name__ == '__main__':
sys.path.append(tools.get_run_folder())
# Import all sub path without out and archive
for folder in os.listdir("."):
	if os.path.isdir(folder)==True:
		if     folder.lower()!="android" \
		   and folder.lower()!="archive" \
		   and folder.lower()!="out" :
			debug.debug("Automatic load path: '" + folder + "'")
			module.import_path(folder)
start()



