## dictool.py ##################################################################
## autoprint dicts #############################################################
################################################################################

def getValueFormattedByDepth(someValue, depth):
	if(depth > 0):
		output = "	"*depth
	else:
		output = ""
	return "%s%s" % (output, someValue)

def printDictTree(someDict, depth=0):
	if(type(someDict) == dict):
		for key in someDict:
			if(type(someDict[key]) == dict):
				print getValueFormattedByDepth(key, depth)
				printDictTree(someDict[key], depth+1)
			else:
				print getValueFormattedByDepth("%s: %s" % (key, repr(someDict[key])), depth)
	else:
		print getValueFormattedByDepth(someDict, depth)


if(__name__ == "__main__"):
	demoDict = {'12617': {'Score': 'lost 1 - 2', 'thisTeamName': 'Goon Squad', 'S.O.C.': '2', 'Opposing Team': 'Sloppy-Serves', 'Location': 'Physical Activities Complex: Gym: Court 1', 'dateTimeString': 'Sun Nov 8 @ 9:30 pm', 'scoreDictionary': {'loserScore': 1, 'thisTeamResult': 'lost', 'winnerScore': 2}}, '12707': {'Score': 'won 1 - 2', 'thisTeamName': 'Sloppy-Serves', 'S.O.C.': '3', 'Opposing Team': 'Goon Squad', 'Location': 'Physical Activities Complex: Gym: Court 1', 'dateTimeString': 'Sun Nov 8 @ 9:30 pm', 'scoreDictionary': {'loserScore': 1, 'thisTeamResult': 'won', 'winnerScore': 2}}}
	printDictTree(demoDict)

