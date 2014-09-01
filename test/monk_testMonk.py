#!/usr/bin/python
import monkModule
import monkTools as tools

def get_desc():
	return "monk test all element that is capable"

def create():
	# module name is 'ewol' and type binary.
	myModule = monkModule.Module(__file__, 'testMonk', 'LIBRARY')
	# enable doculentation :
	myModule.set_website("http://heeroyui.github.io/monk/")
	myModule.set_website_sources("http://github.com/heeroyui/monk/test/")
	myModule.set_path(tools.get_current_path(__file__))
	myModule.set_path_general_doc(tools.get_current_path(__file__) + "/../doc/")
	# add the currrent module at the 
	return myModule

