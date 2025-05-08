def iteration_core(custom, iteratorIdx):
    degree = ""
    func = ""
    dep_unsanitized = ""
    is_name = False
    if(iteratorIdx>0 and custom[iteratorIdx-1]=='['):
        while(custom[iteratorIdx] != ']'):
            degree+= custom[iteratorIdx]
            iteratorIdx+=1
        iteratorIdx += 2
    if(iteratorIdx==0 and '(' not in custom):
        return custom
    if(iteratorIdx==0 and '(' in custom):
        while(custom[iteratorIdx]!='('):
            iteratorIdx+=1
        iteratorIdx+=1
        is_name=True
    openCount = 1
    while (openCount):
        if(custom[iteratorIdx] == '('):
            openCount += 1
        elif (custom[iteratorIdx] == ')'):
            openCount -= 1
        if(openCount):
            func += custom[iteratorIdx]
        iteratorIdx += 1
    if(is_name):
        return convert(func)
    iteratorIdx += 1
    openCount=1
    while(openCount):
        if(custom[iteratorIdx]=='['):
            openCount+=1
        elif(custom[iteratorIdx]==']'):
            openCount-=1
        if(openCount):
            dep_unsanitized+= custom[iteratorIdx]
        iteratorIdx += 1
    iteratorIdx-=1
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
            dep_sanitized += ' \\partial ' + convert(dep_list[i])+'^'+ str(degree_cpy)
        elif (not i):
            dep_sanitized += '\\partial ' + convert(dep_list[i])
        else:
            dep_sanitized += ' \\partial ' + convert(dep_list[i])
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
            dep_sanitized += ' d' + convert(dep_list[i])+'^'+ str(degree_cpy)
        elif (not i):
            dep_sanitized += 'd' + convert(dep_list[i])
        else:
            dep_sanitized += ' d' + convert(dep_list[i])
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
    return '\\frac{' + func + '}{' + convert(dep_unsanitized) + '}'

def piece_handler(custom, iteratorIdx):
    # print(custom[iteratorIdx]) #']' output
    #Piece[if(lhs>=rhs) => (f(x)); ](func_name)
    unsanitized_inp = ""
    openCount = 1
    name=""

    while(openCount):
        if(custom[iteratorIdx]=='['):
            openCount+=1
        elif(custom[iteratorIdx]==']'):
            openCount-=1
        if(openCount):
            unsanitized_inp+= custom[iteratorIdx]
        iteratorIdx+=1
    openCount=1
    while(iteratorIdx<len(custom)):
        if(custom[iteratorIdx]==')'):
            openCount-=1
        elif(custom[iteratorIdx]=='('):
            openCount+=1
        if(openCount):
            name+= custom[iteratorIdx]
        iteratorIdx+=1
    name=name[1:len(name)-1]
    inner= iteration_core(name,0)
    if('(' in name):
        sections=[]
        part=""
        it=0
        while (it < len(name)):
            part+= name[it]
            openCountInt=0
            if(name[it]=='(' and not openCountInt):
                if(part[-1]=='('):
                    part = part[:len(part)-1] + '\\left('
                if(part[0]==')'):
                    part = part[1:] + '\\right)'
                sections.append(part)
                part=""
                openCountInt=1
                while(openCountInt):
                    it+=1
                    if(name[it]==')'):
                        openCountInt-=1
                    elif(name[it]=='('):
                        openCountInt+=1
                it-=1
                sections.append(inner)
            it+=1
        if(part[-1]=='('):
            part = part[:len(part)-1] + '\\left('
        if(part[0]==')'):
            part = part[1:] + '\\right)'       
        sections+= part
        inner =""
        for section in sections:
            inner+= section
    output=inner+ '= \\begin{cases} '

    listOfCond = unsanitized_inp.split(';')
    for i in range(len(listOfCond)):
        cond, then = listOfCond[i].split('=>')
        cond = cond[1:len(cond)-1]
        then = convert(then)
        if(i==len(listOfCond)-1):
            output+= then + ' ,& ' + cond
        else:
            output+= then + ' ,& ' + cond +  "\\" + "\\ "
    output+= '\\end{cases}' 
    return output


def matrix_handler(custom, iteratorIdx, switch):
    # Syntax: 'Mx([1,2,3];[4,5,6];[7,8,9])'
    raw_data = custom[3:len(custom)-1]
    listOfRow = raw_data.split(';')
    if(not switch):
        output = '\\begin{bmatrix} '
    else:
        output = '\\begin{vmatrix}'
    for index in range(len(listOfRow)):
        listOfRow[index] = listOfRow[index][1:len(listOfRow[index])-1].split(',')
        for ind2 in range(len(listOfRow[index])):
            if(ind2!= len(listOfRow[index])-1):
                output+= convert(listOfRow[index][ind2]) + ' &'
            else:
                output+= convert(listOfRow[index][ind2])
        if(index!= len(listOfRow)-1):
            output+= ' \\' + '\\'
    if(not switch):
        output+= ' \\end{bmatrix}'
    else:
        output+= ' \\end{vmatrix}'
    return output

def sqrt_handler(custom, iterationIdx):
    #Sqrt[deg](fun)
    iterationIdx-=1
    print(iterationIdx)
    output = "\\sqrt"
    if(custom[iterationIdx]=='['):
        degree=""
        openCount = 1
        iterationIdx+=1
        while(openCount):
            if(custom[iterationIdx] in '[('):
                openCount+=1
            elif(custom[iterationIdx] in ')]'):
                openCount-=1
            if(openCount):
                degree += custom[iterationIdx]
            iterationIdx+=1
    else:
        degree="1"
    iterationIdx+=1
    degree= convert(degree)
    openCount=1
    func = ""
    while(openCount):
        if(custom[iterationIdx] in '[('):
            openCount+=1
        elif(custom[iterationIdx] in ')]'):
            openCount-=1
        if(openCount):
            func += custom[iterationIdx]
        iterationIdx+=1
    func = convert(func)
    if(degree=='1'):
        output+='{' + func + '}'
    else:
        output+= '['+degree+']{'+func+'}'
    return output



def convert(custom):
    listOfExp = []
    temp=""
    isInner = False
    openCount=0
    for i in range(len(custom)):
        if(custom[i] in '(['):
            openCount+=1
        elif(custom[i] in ')]'):
            openCount-=1
        if(not openCount):
            isInner = False
        else:
            isInner = True
        if('Piece' in custom):
            listOfExp=[custom]
            break
        if((custom[i]==']' and i<len(custom)-1 and custom[i+1]== ' ') and temp != "" and not isInner):
            temp+= custom[i]
            listOfExp.append(temp)
            temp= ""
        elif((custom[i] in 'PDIFT' and i>0 and custom[i-1]==" " and not isInner)):
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
        case "Tht":
            return '\\theta'
        case "Piece":
            return piece_handler(custom, iteratorIdx)
        case "Mx":
            return matrix_handler(custom, iteratorIdx, 0)
        case "Dt":
            return matrix_handler(custom, iteratorIdx, 1)
        case "Sqrt":
            return sqrt_handler(custom, iteratorIdx)
            
        
    return custom

while(True):
    print(convert(input("syntax: ")))
