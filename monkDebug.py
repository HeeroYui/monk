#!/usr/bin/python
import os

debugLevel=3
debugColor=False

color_default= ""
color_red    = ""
color_green  = ""
color_yellow = ""
color_blue   = ""
color_purple = ""
color_cyan   = ""


def set_level(id):
	global debugLevel
	debugLevel = id

def enable_color():
	global debugColor
	debugColor = True
	global color_default
	color_default= "\033[00m"
	global color_red
	color_red    = "\033[31m"
	global color_green
	color_green  = "\033[32m"
	global color_yellow
	color_yellow = "\033[33m"
	global color_blue
	color_blue   = "\033[34m"
	global color_purple
	color_purple = "\033[35m"
	global color_cyan
	color_cyan   = "\033[36m"

def verbose(input):
	global debugLock
	global debugLevel
	if debugLevel >= 5:
		print(color_blue + input + color_default)

def debug(input):
	global debugLock
	global debugLevel
	if debugLevel >= 4:
		print(color_green + input + color_default)

def info(input):
	global debugLock
	global debugLevel
	if debugLevel >= 3:
		print(input + color_default)

def warning(input):
	global debugLock
	global debugLevel
	if debugLevel >= 2:
		print(color_purple + "[WARNING] " + input + color_default)

def error(input, threadID=-1):
	global debugLock
	global debugLevel
	if debugLevel >= 1:
		print(color_red + "[ERROR] " + input + color_default)
	exit(-1)

def print_element(type, lib, dir, name):
	global debugLock
	global debugLevel
	if debugLevel >= 3:
		print(color_cyan + type + color_default + " : " + color_yellow + lib + color_default + " " + dir + " " + color_blue + name + color_default)


