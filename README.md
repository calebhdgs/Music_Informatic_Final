# Music_Informatic_Final

    I have been trying to make the jumping algorithm in Infinite Playlist less random.To do this, I have made a few methods that can be called to switch the behavior of the jumps.     
    I don't like how the branchLessTaken requires me to know how much each beat has been played, and I'm passing the count of each possible end branch in a list as a parameter. This seems like a very inefficient way to find how many times each beat has been played.    
    The next method I am working on is LessRepeatBranch which has the average # of times a beat has been played. if the branch leads to a beat that has been played more than this, it does not take it, leaving only branches that lead to less played sections as viable jumps. I am going to run into the same problem here as I did with the last one. I need to figure out a way to obtain the number of times a specific beat was played in a better manner.
```
def class BranchChoice:

    def randomBranch(candidates, prob):
        if random() < prob:
            branch = choice(candidates)
            return branch
        return NULL

    def findTimesPlayed(beat):

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
