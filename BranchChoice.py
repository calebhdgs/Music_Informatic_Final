#Author: Caleb Hodges

#This class replaces the random branches in the infinite jukebox
#with branches that are a little more deliberate.

from random import randint
from random import choice

#helper methods

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
    e = []			#our list that holds all the edges
    count = []      #the list that will hold our beat counts

    def __init__(self, e):
		self.e = e 
		count = []
		self.count = count
		for md5 in e:						#the md5 and beat_1 variables are keys
			#print md5
			for beat_1 in e[md5]:
				#print beat_1
				for edge in e[md5][beat_1]: #use the keys to pull out the edges
					#print edge
					repeat = 0				
					dst = edge[0]
					md5_2 = edge[1]
					beat_2 = edge[2]
					for tup in count:		#check to see if the beat is already in count
						if tup[0] == md5_2 and tup[1] == beat_2:
							repeat = 1					#then the beat is a repeat and we don't add it to count
					if repeat == 0:             		#If it is not a repeat, 
						lst = [md5_2, beat_2, 0]        #we put it in a list with 0
						count.append(lst)				#and apppend it to count
		print ""

    #Method: randomBranch
    #Parameters: self - the class
	#			 md5 - the key that corresponds to the current song in e[]
	#			 beat - the number of the currently playing beat
    #Returns: an edge vector (distance, md5_2, beat_2)
    #Description: randomly branches to any available edge
    
    def randomBranch(self, md5, beat):
        incrementBeat(self, md5, beat)     	#increment the current beat
        possibleBranches = getEdges(self, md5, beat)
        branch = choice(possibleBranches) 	#randomly pick an edge
        print branch, "***CHOSEN***"
        return branch                   	#and return it
    
    #Method: branchLessTaken
    #Parameters: self - the class
	#			 md5 - the key that corresponds to the current song in e[].
	#			 beat - the number of the currently playing beat
    #Returns: an edge vector (distance, md5_2, beat_2)
    #Description: branches to the edge that ends in the least played beat.

    def branchLessTaken(self, md5, beat):
		incrementBeat(self, md5, beat)     	#increment current beat
		possibleBranches = getEdges(self, md5, beat)
		goodTransitions = []
		lowest = findTimesPlayed(self, possibleBranches[0][1], possibleBranches[0][2])
		for edge in possibleBranches:		#find how many times each beat has been played and put it into a list
			#print edge
			end_md5 = edge[1]
			end_beat = edge[2]             #get the end beat
			timesPlayed = findTimesPlayed(self, end_md5, end_beat) #and find how many times it has been played
			if timesPlayed < 0 :
				break
			elif timesPlayed < lowest:		#If the number of times played is less than the lowest,
				del goodTransitions[:]		#erase the list and add the current edge
				goodTransitions.append(edge)
			elif timesPlayed == lowest:
				goodTransitions.append(edge)
        #return a branch with the least played beat
		if len(goodTransitions) == 0:
			ret = possibleBranches[0]
			print ret, "***ERROR HAS OCCURED***"
			return ret
		else:
			ret = choice(goodTransitions)
			for i in possibleBranches:
				print i, findTimesPlayed(self, i[1], i[2])
			print ret, findTimesPlayed(self, ret[1], ret[2]), "***CHOOSEN***"
			print choice(possibleBranches), "***RANDOM CHOICE***"
			return ret

    #Method: lessRepeatBranch
    #Parameters: self - the class
	#			 md5 - the key that corresponds to the current song in e[].
	#			 beat - the number of the currently playing beat
    #Returns: an edge vector (distance, md5_2, beat_2)
    #Description: finds branches that lead to beats that have been played less than average,
	#			  and then randomly chooses one

    def lessRepeatBranch(self, md5, beat):
        avg = findAverageBeatsPlayed(self)					#find the number an average beat has been played
        goodTransitions = []
        possibleBranches = getEdges(self, md5, beat)
        incrementBeat(self, md5, beat)
        for e in possibleBranches:         					#pull out an edge
            timesPlayed = findTimesPlayed(self, e[1], e[2])	#and find how many times it's been played
            if timesPlayed <= avg and timesPlayed > -1:    	#if it is below the average
				print e, timesPlayed
				goodTransitions.append(e)   				#append the edge to possibleTransitions
        if len(goodTransitions) == 0:
			print "No Good Transitions. Continuing to play"
			return [0, md5, beat]						#If no good transitions, return the current edge vector
        else:
			ret = choice(goodTransitions)  				#randomly choose an edge to transit
			print ret, findTimesPlayed(self, ret[1], ret[2]), avg, "***CHOICE***"
			return ret

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
		for l in possibleBranches:			#pull out each edge
			print l, l[0]
			if l[0] < shortest:				#if it has the shortest distance,
				del goodTransitions[:]		#erase the old list of transitions
				goodTransitions.append(l)	#and add the new edge in
			elif l[0] == shortest:
				goodTransitions.append(l)	#if it is just as long, append the edge
		if len(goodTransitions) == 0:
			ret = possibleBranches[0]		#Failsafe, since edges are ordered by their first element
			print ret
		else:
			ret = choice(goodTransitions)	#return a random edge with the lowest distance
			print ret, ret[0], "***CHOICE***"
			return ret
