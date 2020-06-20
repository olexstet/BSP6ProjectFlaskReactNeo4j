# use for finding all possible paths 
def formPaths(paths,synsetInit): # paths and the intial term 
    result = []
    previousHyp = None
    for value,synset in paths:
        if synset != synsetInit:
            length = len(paths[(value,synset)])

            addedArray = []
            previousWord = synset
            previousArray = []
            for array in result: # go through all possible paths  
                previous = array[len(array)-1]
                dist = 0
                for (v,syn) in paths:
                    if syn == previous:
                        dist = v

                if synset in paths[(dist,previous)] and previous not in previousArray:
                    array.append(synset)
                    addedArray = array
                    previousArray += [previous]
                    
            for j in range(length-1):
                result.append(addedArray.copy())
                
        else: # if initial term  
            length = len(paths[(value,synset)])
            while length > 0:
                result.append([synset]) # add initial term 
                length -= 1

    
    return result
