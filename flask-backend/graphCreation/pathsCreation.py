def formPaths(paths,synsetInit):
    result = []
    previousHyp = None
    for value,synset in paths:
        if synset != synsetInit:
            length = len(paths[(value,synset)])

            addedArray = []
            previousWord = synset
            previousArray = []
            for array in result: 
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
                
        else:
            length = len(paths[(value,synset)])
            while length > 0:
                result.append([synset])
                length -= 1

    
    return result