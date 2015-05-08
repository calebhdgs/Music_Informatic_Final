#Author: Caleb Hodges

#This class replaces the random branches in the infinite jukebox
#with branches that are a little more deliberate.

from random import randint
from random import choice

def getEdges(self, md5, beat):
    return self.e[md5][beat]

def findTimesPlayed(self, md5, beat):
    for b in self.count:
        if b[0] == md5 and b[1] == beat:
            timesPlayed = b[2]
            return timesPlayed
    return -1

def incrementBeat(self, md5, beat):
    for b in self.count:
        if b[0] == md5 and b[1] == beat: 
            #print "Found the correct beat in count"
            val = b[2]+1
            b[2] = val
            return 1
    return -1

def findAverageBeatsPlayed(self):
	sum = 0
	for l in self.count:
		sum += l[2]
	avg = sum/len(self.count)
	return avg
	
class BranchChoice:
    e = []          #our list that holds all the edges
	#e[md5_1][beat#] = [dist, md5_2, beat#]
	#max dst = 80
    count = []    #the list that will hold our beat counts

    def __init__(self, e):
		self.e = e 
		count = []
		self.count = count
		for md5 in e:
			#print md5
			for beat_1 in e[md5]:
				#print beat_1
				for edge in e[md5][beat_1]:
					#print edge
					repeat = 0
					dst = edge[0]
					md5_2 = edge[1]
					beat_2 = edge[2]
					for tup in count:
						if tup[0] == md5_2 and tup[1] == beat_2:
							repeat = 1			#then the beat is a repeat and we don't add it to count
					if repeat == 0:             #If it is not a repeat, 
						lst = [md5_2, beat_2, 0]       #we put it in a list with 0
						count.append(lst)	#and apppend it to count
		print ""

    #Method: randomBranch
    #Parameters: self - the class
	#			 md5 - the key that corresponds to the current song in e[]
	#			 beat - the number of the currently playing beat
    #Returns: an edge vector (distance, md5_2, beat_2)
    #Description: randomly branches to any available edge
    
    def randomBranch(self, md5, beat):
        incrementBeat(self, md5, beat)     #increment the current beat
        #r = randint(0, 100)
        #if (rand <= prob):                  #decide if we will take a branch at all
        possibleBranches = getEdges(self, md5, beat)
        branch = choice(possibleBranches) #randomly pick an edge
        return branch                   	 #and return it
        #else:
        #    return NULL                     #else, return NULL
    
    #Method: branchLessTaken
    #Parameters: self - the class
	#			 md5 - the key that corresponds to the current song in e[].
	#			 beat - the number of the currently playing beat
    #Returns: an edge vector (distance, md5_2, beat_2)
    #Description: branches to the edge that ends in the least played beat.

    def branchLessTaken(self, md5, beat):
		incrementBeat(self, md5, beat)     #increment current beat
		possibleBranches = getEdges(self, md5, beat)
		goodTransitions = []
		lowest = findTimesPlayed(self, possibleBranches[0][1], possibleBranches[0][2])
		for edge in possibleBranches:
			#print edge
			end_md5 = edge[1]
			end_beat = edge[2]             #get the end beat
			timesPlayed = findTimesPlayed(self, end_md5, end_beat) #and find how many times it has been played
			if timesPlayed < 0 :
				break
			elif timesPlayed < lowest:
				del goodTransitions[:]
				goodTransitions.append(edge)
			elif timesPlayed == lowest:
				goodTransitions.append(edge)
            #Find the branch that goes to the least played beat
            #return the branch to least played beat
		if len(goodTransitions) == 0:
			ret = possibleBranches[0]
			print ret
			return ret
		else:
			ret = choice(goodTransitions)
			for i in possibleBranches:
				print i, findTimesPlayed(self, i[1], i[2])
			print ret, findTimesPlayed(self, ret[1], ret[2]), "***CHOOSEN***"
			return ret

    #Method: lessRepeatBranch
    #Parameters: self - the class
	#			 md5 - the key that corresponds to the current song in e[].
	#			 beat - the number of the currently playing beat
    #Returns: an edge vector (distance, md5_2, beat_2)
    #Description: finds branches that lead to beats that have been played less than average,
	#			  and then randomly chooses one

    def lessRepeatBranch(self, md5, beat):
        avg = findAverageBeatsPlayed(self)
        goodTransitions = []
        possibleBranches = getEdges(self, md5, beat)
        incrementBeat(self, md5, beat)
        for e in possibleBranches:         					#pull out an edge
            timesPlayed = findTimesPlayed(self, e[0], e[1])
            if timesPlayed <= avg and timesPlayed > -1:    	#if it is below the average
                goodTransitions.append(e)   			#append the edge to possibleTransitions
        if len(goodTransitions) == 0:
            return possibleBranches[0]
        else:
            return choice(goodTransitions)  				#randomly choose an edge to transition

	#Method: smoothestBranch
	#Parameters: self - the class
	#			 md5 - the key that corresponds to the current song in e[].
	#			 beat - the number of the currently playing beat
    #Returns: an edge vector (distance, md5_2, beat_2)
	#Description: picks the transition with the shortest distance
	
	def smoothestBranch(self, md5, beat):
		possibleBranches = getEdges(self, md5, beat)
		incrementBeat(self, md5, beat)
		goodTransitions = []
		shortest = possibleBranches[0][0]
		for l in possibleBranches:
			print l, l[0]
			if l[0] < shortest:
				del goodTransitions[:]
				goodTransitions.append(l)
			elif l[0] == shortest:
				goodTransitions.append(l)
		if len(goodTransitions) == 0:
			ret = possibleBranches[0]
			print ret
		else:
			ret = choice(goodTransitions)
			print ret, ret[0], "***CHOICE***"
			return ret
