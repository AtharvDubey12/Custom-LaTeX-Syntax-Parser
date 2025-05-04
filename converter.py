def iteration_core(custom, iteratorIdx):
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
    func = convert(func)
    if(func[0]=='('):
        func = '\\left' + func[:len(func)-1] + '\\right)'
    return (degree, degree_cpy, func, dep_unsanitized, iteratorIdx)



def pdiff_handler(custom, iteratorIdx):
    # syntax example: Pdiff[2](x)[x,y]
    degree, degree_cpy, func, dep_unsanitized,_ = iteration_core(custom, iteratorIdx)
    dep_list = dep_unsanitized.split(',')
    if(degree_cpy>1):
        num_sanitized ="\\frac{\\partial^" + str(degree_cpy) +" "+ func
    else:
        num_sanitized ="\\frac{\\partial " + func 
    num_sanitized+='}'
    dep_sanitized = '{'
    for i in range(len(dep_list)):
        if(i==len(dep_list)-1 and degree_cpy>1):
            dep_sanitized += ' \\partial ' + dep_list[i]+'^'+ str(degree_cpy)
        elif (not i):
            dep_sanitized += '\\partial ' + dep_list[i]
        else:
            dep_sanitized += ' \\partial ' + dep_list[i]
        degree_cpy -= 1
    dep_sanitized += '}'

    return num_sanitized+dep_sanitized


def diff_handler(custom, iteratorIdx):
    # syntax example: Diff[2](x)[x,y]
    degree, degree_cpy, func, dep_unsanitized,_ = iteration_core(custom, iteratorIdx)
    dep_list = dep_unsanitized.split(',')
    if(degree_cpy>1):
        num_sanitized ="\\frac{d^" + str(degree_cpy) +" "+ func
    else:
        num_sanitized ="\\frac{d" + func 
    num_sanitized+='}'
    dep_sanitized = '{'
    for i in range(len(dep_list)):
        if(i==len(dep_list)-1 and degree_cpy>1):
            dep_sanitized += ' d' + dep_list[i]+'^'+ str(degree_cpy)
        elif (not i):
            dep_sanitized += 'd' + dep_list[i]
        else:
            dep_sanitized += ' d' + dep_list[i]
        degree_cpy -= 1
    dep_sanitized += '}'
    return num_sanitized+dep_sanitized


def integ_handler(custom, iteratorIdx):
    # syntax example: Integ[2](x)[x]
    degree, degree_cpy, func, dep_unsanitized, iteratorIdx = iteration_core(custom, iteratorIdx)
    iteratorIdx+=1
    if('->' in custom):
        return definteg_handler(custom, iteratorIdx,degree_cpy, func, dep_unsanitized)
    dep_list = dep_unsanitized.split(',')
    num_sanitized = '\\'
    for i in range(degree_cpy):
        num_sanitized+='i'
    num_sanitized += 'nt ' + func + ' \\, '
    for object in dep_list:
        num_sanitized += 'd' + object + '\\,'
        degree_cpy -= 1
    while(degree_cpy):
        num_sanitized+= 'd' + dep_list[-1] + '\\,'
        degree_cpy -= 1
    return num_sanitized[:len(num_sanitized)-2]

def definteg_handler(custom, iteratorIdx,degree_cpy, func, dep_unsanitized):
    # example syntax: integ[3](x)[x,y,z][0->1,0->2,0->3]

    dep_list = dep_unsanitized.split(',')
    lim_str = ""
    iteratorIdx+=1
    while(iteratorIdx != len(custom)-1):
        lim_str+= custom[iteratorIdx]
        iteratorIdx += 1
    num_sanitized = ""
    lims = lim_str.split(',')[::-1]
    for i in range(len(lims)):
        num_sanitized += '\\int_{' + convert(lims[i].split('->')[0]) + '}^{' + convert(lims[i].split('->')[1]) + '} '
    num_sanitized+= func + ' '
    for object in dep_list:
        num_sanitized+= '\\, d' + object + ' '
        degree_cpy-=1
    while(degree_cpy):
        num_sanitized+= '\\, d' + dep_list[-1] + ' '
        degree_cpy-=1
    
    return num_sanitized

def frac_handler(custom, iteratorIdx):
    _, _, func, dep_unsanitized,_ = iteration_core(custom, iteratorIdx)
    func = convert(func)
    return '\\frac{' + func + '}{' + dep_unsanitized + '}'


def convert(custom):
    listOfExp = []
    # just think of a working splitting logic and rest is working perfectly recursion wise
    temp=""
    for i in range(len(custom)):
        if((custom[i]==']' and i<len(custom)-1 and custom[i+1]== ' ') and temp != ""):
            temp+= custom[i]
            listOfExp.append(temp)
            temp= ""
        elif(custom == '1+Pdiff(x)[y]'):
            listOfExp=['1+', 'Pdiff(x)[y]']
            break
        elif((custom[i] in 'PDI' and i>0 and custom[i-1]==" ")):
            listOfExp.append(temp)
            temp=custom[i]
        elif (temp != "" and i==len(custom)-1):
            temp+= custom[i]
            listOfExp.append(temp)
        else:
            temp+= custom[i]
    if(len(listOfExp)>1):
        for i in range(len(listOfExp)):
            if(ord(listOfExp[i][0])>=65 and ord(listOfExp[i][0])<86):
                listOfExp[i]= convert(listOfExp[i])
        ret=""
        for x in listOfExp:
            ret+= x
        return ret
    elif(len(listOfExp)==1):
        custom = listOfExp[0]       
    if(not len(custom)):
        return custom
    keyword=""
    iteratorIdx = 0
    capture_flag = False
    while(iteratorIdx<len(custom)):
        if(custom[iteratorIdx].isalpha()):
            capture_flag= True
        elif(not custom[iteratorIdx].isalpha() and keyword != ""):
            break
        if(capture_flag):
            keyword+= custom[iteratorIdx]
        iteratorIdx+=1
    iteratorIdx+=1

    match(keyword):
        case "Pdiff":
            return pdiff_handler(custom, iteratorIdx)
        case "Diff":
            return diff_handler(custom, iteratorIdx)
        case "Integ":
            return integ_handler(custom, iteratorIdx)
        case "Frac":
            return frac_handler(custom, iteratorIdx)
        case "Pi":
            return '\\pi'
        
    return custom 

                


while(True):
    try:
        syntax = input("enter syntax: ")
        print(convert(syntax))
    except:
        print(syntax)
    