# Music_Informatic_Final

##Problem     
The Infinite Jukebox has a few problems with it’s branching algorithm. It disproportionately plays heavily branched areas more than areas that have few branches. This is because some parts of songs are very similar and loop back in on themselves frequently, forming a sort of “cluster”. These clusters tend to repeat a sequence that sounds very similar, leading to much less variety than desired from a randomly branching algorithm. How can we make an algorithm that jumps randomly, while choosing to take certain transitions over others?
      
##Questions
How do we tell which beats have been played more than others?
   
Can I make it so that others could add their own Branching algorithm with little interference to my own code?
   
What should be the deciding factor when choosing NOT to take a branch?

##Resources
Perry's Infinite playlist
   
Luke Stack's Spotify Interface and contributions to Perry’s InfinitePlaylist

##Abstract
I decided to make my program a class that can be created by the coder and then used to call whatever branching method they want. This allows the coder to create and call their own method without modifying existing code.  The class itself takes the edges file in the pickle object as a parameter. I added four methods that affect the behavior of the branching algorithm in a specific way. 

##Methods
All branching methods take a key that identifies the currently playing song and the current beat number. All methods return an edge vector that contains the distance from the current beat to the beat that will be transitioned to, the key that identifies the new song that will be playing, and the beat of the song that will be playing.
   
The first method is randomBranch. This method is the vanilla branch that works the same as the currently implemented random branch algorithm. It simply identifies possible branches for the current beat and chooses one at random.
   
The next method is branchLessTaken. This method identifies all possible branches from the current beat and creates a list of possible transitions whose ending beat has been played the fewest times. For this method, I had to implement a way to keep track of how many times each beat had been played. I settled for knowing only how many times the beats I was transitioning to or from were played. This is not entirely accurate as I am transitioning to the beat after the beat I am looking at, but theoretically, the same principle holds. If it is a high traffic area, the beat I am looking at will be played more than others, and so should cancel out my inaccuracy. The benefits of using this method is that there is more variety when the track is playing. The drawbacks of using this method is that if there is only one possible branch, It will take the branch, since it is the least played of the possible transition. So this method does not work well for clusters of beats with single possible transitions. Conversely, this method works very well for beats that have a large number of possible transitions.
   
The next method, lessRepeatBranch, aims to fix the previous issue. It keeps track of the number of times an average beat will have been played. If the number of times the end of the branch has been played is above the average, then that branch will not be taken. To avoid picking the first branch that satisfies this condition, we place all possible transitions into a list and randomly choose one from the list. The benefits of using this method is that it will always break out of clusters when possible, or simply play its way out without taking any transitions. The drawbacks is that there may be fairly long sections where no transition is found that is acceptable, so no branches will be taken. This method works well with heavily mapped areas, since it will lead to areas that haven’t been played recently, but does not work well with songs that are not mapped heavily, since very few branches will be taken.
   
The final method is not random, but is something I added on a whim. SmoothestBranch finds the transition with the end beat that has the shortest distance to the one currently being played. For Perry’s InfinitePlaylist, this would be the first possible transition since edges are sorted by their first element. However, I don’t want to rely on this, so I made my method search through all possible transitions to find the shortest distance. This method will always take the same branch, so there is no variety, but the transitions will be slightly smoother.

##Results
The results of the randomBranch method were inconclusive. There is no way to tell if there is a pattern to the algorithm’s choice.
   
The results of the branchLessTaken method were good. It would always take one of the least taken branches, but sometimes there was only one branch that was highly played, and it would still take it, since it was the only one.
   
The results of the lessRepeatBranch were hard to gauge. It does seem to be working since braches were both taken that had a beat count of less than average, and some transitions were avoided altogether. That being said, due to the nature of the method, it needs to be tested for extended periods of time. I ran it for close to ten minutes, with only 300 seconds of audio being played, but there were still some beats that had not been played. This was interesting since the entire playlist could have been played twice. However, It is possible that the branches just happened to not be taken. Therefore, I am only 80% sure this method works perfectly. Further hours of testing should be done, but I am fairly confident that it does work.
   
The results of the smoothestBranch were perfect. every transition takes the shortest branch available to it.

