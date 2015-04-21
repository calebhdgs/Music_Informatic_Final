# Music_Informatic_Final

I have been trying to make jumping algorithm in Infinite Playlist less random.
To do this, I have made a few methods that can be called to switch the behavior of the jumps.
So far I have replicated the random branch algorithm and made most of the branchLessTaken Algorithm.
I haven't finished the branchLessTaken because it requires me to know how much each beat has been played, and I can't find that information out without altering the existing code or passing the count of each and every in a list as a parameter, which wouldn't make this method very efficient. 
The next method I will be working on is LessRepeatBranch which will have the average # of times a beat has been played. if the branch leads to a beat that has been played more than this, it does not take it, leaving only branches that lead to less played sections as viable jumps. I am going to run into the same problem here as I did with the last one. I need to figure out a way to obtain the number of times a specific beat was played.
```
def class BranchChoice:

    def randomBranch(candidates, prob):
        if random() < prob:
            branch = choice(candidates)
            return branch
        return NULL

    def findTimesPlayed(beat):

    def branchLessTaken(candidates, prob):
        #I want to branch to the beat that has been played the least
        #To do this, I need to know how many times each end beat has been played

        #make sure you are actually branching
        if random() < prob:
            possibleBranchTimesPlayed = []
            #for each beat that we could transition to,
            #get the number of times it has been played
            for edge in candidates:
                beat = edge[2];
                timesPlayed = findTimesPlayed(beat)
                possibleBranchTimesPlayed.append(timesPlayed)
            lowest = possibleBranchTimesPlayed[0]
            lowestIndex = 0
            i=0
            #Find the brach that goes to the least played beat
            while i < len(possibleBranchTimesPlayed):
                if possibleBranchTimesPlayed[i] < lowest:
                    lowest = possibleBranchTimesPlayed[i]
                    lowestIndex = i
                i++
            #return the branch to least played beat
            return candidates[i]
        #If we don't branch, return null
        return NULL

    def lessRepeatBranch(candidates, prob):
        #If branches lead to high traffic areas,
        #don't take the branches

```
