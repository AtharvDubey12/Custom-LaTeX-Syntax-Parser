def pdiff_handler(custom, iteratorIdx):
    degree = ""
    func = ""
    dep_unsanitized = ""
    if(custom[iteratorIdx-1]=='['):
        while(custom[iteratorIdx] != ']'):
            degree+= custom[iteratorIdx]
            iteratorIdx+=1
        iteratorIdx += 2
    openCount = 1
    while (openCount):
        if(custom[iteratorIdx] == '('):
            openCount += 1
        elif (custom[iteratorIdx] == ')'):
            openCount -= 1
        if(openCount):
            func += custom[iteratorIdx]
        iteratorIdx += 1
    iteratorIdx += 1
    while(custom[iteratorIdx] != ']'):
        dep_unsanitized+= custom[iteratorIdx]
        iteratorIdx += 1
    if(degree != ""):
        degree_cpy = int(degree)
    else:
        degree_cpy = 1
    if(degree_cpy>1):
        num_sanitized ="\\frac{\\partial^" + str(degree_cpy) +" "+ func
    else:
        num_sanitized ="\\frac{\\partial " + func 
    num_sanitized+='}'
    dep_list = dep_unsanitized.split(',')
    dep_sanitized = '{'
    for i in range(len(dep_list)):
        if(i==len(dep_list)-1 and degree_cpy>1):
            dep_sanitized += ' \\partial ' + dep_list[i]+'^'+ str(degree_cpy)
        elif (i==0):
            dep_sanitized += '\\partial ' + dep_list[i]
        else:
            dep_sanitized += ' \\partial ' + dep_list[i]
        degree_cpy -= 1
    dep_sanitized += '}'
    return num_sanitized+dep_sanitized


def diff_handler(custom, iteratorIdx):
    degree = ""
    func = ""
    dep_unsanitized = ""
    if(custom[iteratorIdx-1]=='['):
        while(custom[iteratorIdx] != ']'):
            degree+= custom[iteratorIdx]
            iteratorIdx+=1
        iteratorIdx += 2
    openCount = 1
    while (openCount):
        if(custom[iteratorIdx] == '('):
            openCount += 1
        elif (custom[iteratorIdx] == ')'):
            openCount -= 1
        if(openCount):
            func += custom[iteratorIdx]
        iteratorIdx += 1
    iteratorIdx += 1
    while(custom[iteratorIdx] != ']'):
        dep_unsanitized+= custom[iteratorIdx]
        iteratorIdx += 1
    if(degree != ""):
        degree_cpy = int(degree)
    else:
        degree_cpy = 1
    if(degree_cpy>1):
        num_sanitized ="\\frac{d^" + str(degree_cpy) +" "+ func
    else:
        num_sanitized ="\\frac{d " + func 
    num_sanitized+='}'
    dep_list = dep_unsanitized.split(',')
    dep_sanitized = '{'
    for i in range(len(dep_list)):
        if(i==len(dep_list)-1 and degree_cpy>1):
            dep_sanitized += ' d' + dep_list[i]+'^'+ str(degree_cpy)
        elif (i==0):
            dep_sanitized += 'd' + dep_list[i]
        else:
            dep_sanitized += ' d' + dep_list[i]
        degree_cpy -= 1
    dep_sanitized += '}'
    return num_sanitized+dep_sanitized






def convert(custom):
    if(not len(custom) or custom[0].upper() != custom[0]):
        return "invalid syntax"
    keyword=""
    iteratorIdx = 0
    while(custom[iteratorIdx]!='[' and custom[iteratorIdx] != '('):
        keyword+= custom[iteratorIdx]
        iteratorIdx+=1
    iteratorIdx+=1

    if(keyword=='Pdiff'):
        return pdiff_handler(custom, iteratorIdx)
    elif(keyword=='Diff'):
        return diff_handler(custom, iteratorIdx)
            

                



syntax = input("enter syntax: ")
print(convert(syntax))
    