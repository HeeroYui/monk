#!/usr/bin/python2.7
# for path inspection:
import sys
import os
import inspect
import fnmatch
import monkDebug as debug
import monkModule
import monkArg
import monkTools



myArg = monkArg.MonkArg()
myArg.add(monkArg.ArgDefine("h", "help", desc="display this help"))
myArg.add_section("option", "Can be set one time in all case")
myArg.add(monkArg.ArgDefine("v", "verbose", list=[["0","None"],["1","error"],["2","warning"],["3","info"],["4","debug"],["5","verbose"]], desc="Display makefile debug level (verbose) default =2"))
myArg.add(monkArg.ArgDefine("C", "color", desc="Display makefile output in color"))

myArg.add_section("cible", "generate in order set")
localArgument = myArg.parse()

##
## @brief Display the help of this makefile
##
def usage():
	# generic argument displayed : 
	myArg.display()
	print("		all")
	print("			Build all (only for the current selected board) (bynary and packages)")
	print("		clean")
	print("			Clean all (same as previous)")
	listOfAllModule = monkModule.list_all_module_with_desc()
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
	for argument in localArgument:
		parse_generic_arg(argument, True)

##
## @brief Run everything that is needed in the system
##
def start():
	actionDone=False
	# parse all argument
	for argument in localArgument:
		if parse_generic_arg(argument, False) == True:
			continue
		if argument.get_option_name() != "":
			debug.warning("Can not understand argument : '" + argument.get_option_name() + "'")
			usage()
		else:
			module = monkModule.get_module(argument.get_arg())
			module.parse_code()
			module.generate()
			actionDone=True
	# if no action done : we do "all" ...
	if actionDone==False:
		#Must generate all docs :
		moduleElements = monkModule.get_all_module()
		for module in moduleElements:
			module.parse_code()
		for module in moduleElements:
			module.generate()

##
## @brief When the user use with make.py we initialise ourself
##
if __name__ == '__main__':
	sys.path.append(monkTools.get_run_folder())
	# Import all sub path without out and archive
	for folder in os.listdir("."):
		if os.path.isdir(folder)==True:
			if     folder.lower()!="android" \
			   and folder.lower()!="archive" \
			   and folder.lower()!="out" :
				debug.debug("Automatic load path: '" + folder + "'")
				monkModule.import_path(folder)
	start()



