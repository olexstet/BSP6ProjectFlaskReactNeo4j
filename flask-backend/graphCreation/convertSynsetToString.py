def convertHypernymsToString(hypernyms):
    result = []
    for hyp in hypernyms: 
        result += [hyp.name().split(".")[0]]

    return result