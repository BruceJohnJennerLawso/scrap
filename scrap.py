## scrap.py ####################################################################
## the scrap console: imported in the standard python interpreter ##############
################################################################################
from sys import argv
from scrapParam import *

import team

import __main__

from distStats import *
from scipy.stats import norm


import statSelect



import teamStatTable
import teamStatGraph
import teamSummary
import readata
import teamStatRanker
import playerSummary
import seasonSummary

def getModulesList():
	return [teamStatTable, teamStatGraph, teamSummary, readata, teamStatRanker, playerSummary, seasonSummary]

def printModulesList():
	for module in getModulesList():
		print module.__name__
		print module
		##print module.moduleId()

def getModuleByName(moduleName):
	for module in getModulesList:
		if(module.__name__ == moduleName):
			return module
	print "Unable to find module named %s, returning empty list instead" % moduleName
	return []
	## intentional crash here

def printModuleDescription(module):
	print module.description()

def modules():
	for module in getModulesList():
		print module.__name__
		
def modulesInfo():
	for module in getModulesList():
		print module.__name__
		print module
		printModuleDescription(module)		
		
def task(module):
	module.task(seasons, params)

def info():
	print "Scrap Version %s" % ("blah")
	flatTeams = [individualTeam for yearTeamList in [season.Teams for season in seasons] for individualTeam in yearTeamList]
	print "Currently loaded %i seasons in %i leagues with %i teams\n" % (len(seasons), len(set([ssn.getLeagueId() for ssn in seasons])), len(flatTeams))	
	print "Available task modules:\n"
	modules()

def help():
	## Oh wont you pleaaaaaase pleaaaaaaaaaaase help meeeee

	print "Scrap Parameters are stored in scrap.params, run scrap.params.info()"
	print "for information about the params\n"
	print "Run scrap.modules() for a list of the available task modules\n"
	print "scrap.[module name].getModuleDescription() for information on what"
	print "each module does\n"
	print "scrap.task([module name]) will run whatever that module is supposed to do"

if(__name__ == "scrap"):
	printTitleBox("The Scrap Project")
	seasons = []
	##seasons += getAllSeasons('watMu', 'beginner') + getAllSeasons('watMu', 'intermediate') + getAllSeasons('watMu', 'advanced') + getAllSeasons('watMu', 'allstar')		
	##seasons += getAllSeasons('wha', 'everything')
	seasons += getAllSeasons('nhl', 'postLockoutCurrent')
	
	params = scrapParams('nhl', 'everything')
	
	if(hasattr(__main__, '__file__')):
		print "scrap imported in external module"
		clearTerminal()
	else:
		clearTerminal()
		printTitleBox("The Scrap Project")
		print "type scrap.help() for information on how to use this module\nscrap.info() for diagnostics"	
	
	
elif(__name__ == "__main__"):
	printTitleBox("The Scrap Project")
	print "The scrap.py module is meant to be run inside of the python"
	print "interpreter, in order to reduce overhead time reloading resources"
	print "with the new seasonParts system\n"
	print "Please run the python interpreter in the directory where scrap is"
	print "located and import scrap to proceed"




