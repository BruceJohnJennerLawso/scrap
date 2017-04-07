## watMuSportInfo.py ###########################################################
## centralizing the dict of info about watMu sports so its #####################
## consistent across the whole stack of iml crawling scripts ###################
################################################################################


def sportsInfoDict():
	return {\
	 28:['soccer', 'outdoor', 'grass', '4-7vs_1GK', 'league'],\
	 4 :['hockey', 'indoor', 'floor', '3-4vs_1GK', 'league'],\
	 3 :['basketball', 'indoor', 'floor', '4-5vs_0GK', 'league'],\
	 5 :['dodgeball', 'indoor', 'floor', '6-8vs_0GK', 'league'],\
	 11:['flag_football', 'outdoor', 'grass', '5-7vs_0GK', 'league'],\
	 7 :['soccer', 'indoor', 'floor', '3-5vs_1GK', 'league'],\
	 1 :['hockey', 'indoor', 'ice', '6-6vs_1GK', 'league'],\
	 31:['ultimate', 'indoor', 'floor', '3-4vs_0GK', 'league'],\
	 10:['slowpitch', 'outdoor', 'grass', '8-10vs_0GK', 'league'],\
	 6 :['soccer', 'outdoor', 'grass', '7-11vs_1GK', 'league'],\
	 2 :['ultimate', 'outdoor', 'grass', '5-7vs_0GK', 'league'],\
	 8 :['volleyball', 'indoor', 'floor', '4-6vs_0GK', 'league'],\
	 17:['soccer', 'indoor', 'floor', '2-3vs_0GK', 'tournament'],\
	 117:['soccer', 'indoor', 'floor', '2-3vs_1GK', 'league'],\
	 26:['basketball', 'outdoor', 'ashphalt', '2-3vs_0GK', 'tournament'],\
	 18:['dodgeball', 'indoor', 'floor', '7-8vs_0GK_hunger_games', 'tournament'],\
	 16:['basketball', 'indoor', 'floor', '2-3vs_0GK', 'tournament']\
	 }
