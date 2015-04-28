# Music_Informatic_Final

##Problem     
I have been trying to make the jumping algorithm in Infinite Playlist less random.To do this, I have made a few methods that can be called to switch the behavior of the jumps.     
##Questions
Since I have a list of all transitions, can I make this handle all aspects of branching?
##Resources
Luke Stack's Spotify Interface      
Perry's Infinite playlist
##Abstract
The class so far takes the edges file in the pickle object. You can then call what branching method you want from the class and it will return a vector containing the edge's data, or a NULL vector if it has decided not to branch. I have three methods that will somewhat randomly take a branch. The first is the true random, which simply returns a possible branch for the beat chosen. The next method, branchLessTaken, picks the least played branch and takes it. The final method, lessRepeatBranch, takes as input a certain number to be used as a limit. If the number of times the end of the branch has been played is above the limit, then that branch will not be taken. To avoid picking the first branch that satisfies this condition, we place all possible transitions into a list and randomly choose one from the list. I would like to implement all branch related methods into this class. From figuring out if a branch is possible, deciding whether or not to branch, and which branch to take.
```
def class BranchChoice(edges): #The pickle file contains a dictionary that holds all the edges 
    self.edges = edges
    def mapBeatsAndEdges(edgeMap):
        for point in range(len(edgeMap)):
            #check and see if the beats are in the list already.
            #if not, add them to the list of beats

    def randomBranch(candidates, prob):
        if random() < prob:
            branch = choice(candidates)
            return branch
        return NULL

    def branchLessTaken(candidates, timesPlayed, prob):
        #I want to branch to the beat that has been played the least
        #To do this, I need to know how many times each end beat has been played

        #make sure you are actually branching
        if random() < prob:
            #the number of times each beat has been played is stored in timesPlayed
            lowest = timesPlayed[0]
            lowestIndex = 0
            i=0
            #Find the brach that goes to the least played beat
            while i < len(timesPlayed):
                if timesPlayed[i] < lowest:
                    lowest = timesPlayed[i]
                    lowestIndex = i
                i++
            #return the branch to least played beat
            return candidates[lowestIndex]
        #If we don't branch, return null
        return NULL

    def lessRepeatBranch(candidates, timesPlayed, averagePlayed, prob):
        #If branches lead to high traffic areas,
        #don't take the branches
        if random() < prob:
            lowestIndex = -1
            lowest = averagePlayed
            i=0
            #find a branch that goes to a low traffic zone.
            while i < len(timesPlayed):
                if timesPlayed[i] < averaePlayed:
                    lowestIndex = i
                    lowest = timesPlayed[i]
                i++
            #If no branch is found that is lower than average, we return null
            if lowestIndex == -1:
                return NULL
            else:
                return candidates[i]
        #If we decide not to branch, return null
        return NULL

```
