# if it exists gaps of levels in sequence, add the missing levels with All property  
def configureSequence(sequence):
    configuredSequence = [sequence[0]]
    for i in range(1,len(sequence)): # if gaps between levels 
        if sequence[i][0]-1 != sequence[i-1][0]:
            step = sequence[i][0] - sequence[i-1][0]
            sequenceToAdd = []
            startValue = sequence[i-1][0] # previous 
            endValue = sequence[i][0]# current 
            for j in range(startValue+1,endValue):
                sequenceToAdd.append([j,"All"]) # add missing level 
            
            configuredSequence += sequenceToAdd + [sequence[i]] # add to existent sequence 
        else:
            configuredSequence += [sequence[i]] # if no gaps in level 
        
    return configuredSequence 
