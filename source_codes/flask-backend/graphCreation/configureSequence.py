def configureSequence(sequence):
    configuredSequence = [sequence[0]]
    for i in range(1,len(sequence)):
        if sequence[i][0]-1 != sequence[i-1][0]:
            step = sequence[i][0] - sequence[i-1][0]
            sequenceToAdd = []
            startValue = sequence[i-1][0]
            endValue = sequence[i][0]
            for j in range(startValue+1,endValue):
                sequenceToAdd.append([j,"All"])
            
            configuredSequence += sequenceToAdd + [sequence[i]]
        else:
            configuredSequence += [sequence[i]]
        
    return configuredSequence 