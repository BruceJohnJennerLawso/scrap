## obfuscant.py ################################################################
## demoing a consistent way of mapping strings to other unique strings that ####
## consist of words ############################################################
################################################################################
from collections import defaultdict
import collections
from string import ascii_lowercase
import random
from random import choice

from random_words import RandomWords
from random_words import RandomNicknames


import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt


random_strings = set()


def random_string():
    while True:
        result = ''.join(choice(ascii_lowercase) for _ in range(6))
        if(result not in random_strings):
            random_strings.add(result)
            return result
			

previouslyGeneratedMaps = {}

def getObfuscatedString(inputString, masks, rw, debugInfo=False):
	if(inputString in previouslyGeneratedMaps):
		return previouslyGeneratedMaps[inputString]
	else:
		currentMaskString = ""
		i = 0
		for character in masks[inputString]:
			if(i == 0):
					
				if(character in "qwertyuiopasdfghjklzcvbnm"):
					wordCharacterMap = rw.random_word(character)
				else:
					wordCharacterMap = character		
				if(debugInfo):
					print character, wordCharacterMap
			else:
				if(character in "qwertyuiopasdfghjklzcvbnm"):
					wordCharacterMap = rw.random_word(character).capitalize()
				else:
					wordCharacterMap = character.capitalize()
				if(debugInfo):
					print character, wordCharacterMap
			i += 1
			currentMaskString += wordCharacterMap
		previouslyGeneratedMaps[inputString] = currentMaskString
		return currentMaskString

def basicTest(masks, rw):	
	names = ["Jim Brooks", "John Lawson", "Jean-Christophe Robertson"]
	
	rawMasks = {}
	
	for name in names:
		rawMasks[name] = masks[name]
	
	rw = RandomWords()
	
	outputMasks = {}
	
	for name in names:
		print(rawMasks[name])	
		
		outputMasks[masks[name]] = getObfuscatedString(name, masks, rw)
		
	for name in names:
		print repr(name), " -> ", repr(rawMasks[name]), " -> ", repr(outputMasks[rawMasks[name]])
	outputs = [outputMasks[rawMasks[name]] for name in names]	
	print len(set(names)), len(set(outputs))
	
	

	# the histogram of the data
	##n, bins, patches = plt.hist([len(name) for name in names], 50, normed=1, facecolor='green', alpha=0.75)

	##plt.xlabel('Name Length (Characters)')
	##plt.ylabel('Probability')
	##plt.title(r'$\mathrm{Histogram\ of\ IQ:}\ \mu=100,\ \sigma=15$')
	##plt.axis([40, 160, 0, 0.03])
	##plt.grid(True)
	
	##plt.show()
	




def randomizedTest(masks, rw):
	fullNames = []
	
	rn = RandomNicknames()
	
	for i in range(400000):
		##print i,
		fNameGender=choice(['f', 'm', 'u'])
		##print fNameGender
		firstNm = rn.random_nick(gender=fNameGender)
		lNameGender=choice(['m', 'u'])
		lastNm = rn.random_nick(gender=lNameGender)
		while([firstNm, lastNm] in fullNames):
			fNameGender=choice(['f', 'm', 'u'])
			firstNm = rn.random_nick(gender=fNameGender)
			lNameGender=choice(['m', 'u'])
			lastNm = rn.random_nick(gender=lNameGender)		
		fullNames.append([firstNm, lastNm])
	rawMasks = {}
	
	names = ["%s %s" % (nm[0], nm[1]) for nm in fullNames]
	
	for name in names:
		rawMasks[name] = masks[name]
	
	rw = RandomWords()
	
	outputMasks = {}
	
	for name in names:
		##print(rawMasks[name])	
		
		outputMasks[masks[name]] = getObfuscatedString(name, masks, rw)
		
	for name in names:
		print repr(name), " -> ", repr(rawMasks[name]), " -> ", repr(outputMasks[rawMasks[name]])

	raws = [rawMasks[name] for name in names]			
	outputs = [outputMasks[rawMasks[name]] for name in names]	
	print len(set(names)), len(set(outputs))
	print [item for item, count in collections.Counter(outputs).items() if count > 1], len([item for item, count in collections.Counter(outputs).items() if count > 1])
	print [item for item, count in collections.Counter(raws).items() if count > 1], len([item for item, count in collections.Counter(raws).items() if count > 1])

	outputDuplicates = [item for item, count in collections.Counter(outputs).items() if count > 1]

	for name in names:
		if(outputMasks[rawMasks[name]] in outputDuplicates):
			print repr(name), " -> ", repr(rawMasks[name]), " -> ", repr(outputMasks[rawMasks[name]])

	# the histogram of the data
	n, bins, patches = plt.hist([len(name) for name in names], 50, normed=1, facecolor='green', alpha=0.75)

	plt.xlabel('Name Length (Characters)')
	plt.ylabel('Probability')
	plt.title(r'$\mathrm{Histogram\ of\ IQ:}\ \mu=100,\ \sigma=15$')
	plt.axis([0, 30, 0, 0.75])
	plt.grid(True)
	
	plt.show()

def getMasks():
	return defaultdict(random_string)

if(__name__ == "__main__"):
	
	random.seed(3141592654)
	masks = getMasks()
	
	rw = RandomWords()
	basicTest(masks, rw)
	randomizedTest(masks, rw)
		
	##print [rw.random_word('b') for i in range(100)]
