# 4 lists to store literal, rules which are added via Tell, derived rules and literals.
literal = []
rule = []
derived = []
total = []


def __main__():
    with open('TMS1.txt') as tms:
        for i in tms:
            action = i.split(':')[1].strip()
            command = i.split(':')[0].strip()
            # if Command is Tell, then we add that to TMS after validation and
            # also check with this we can know other information
            if command == 'Tell':
                # if > not in action means it is a single literal Ex. A, B
                if '>' not in action:
                    # if action is already in literal then it is contradiction and it will not be add to TMS
                    # and loop will continue to next
                    flag1 = True
                    addLiteral(action, flag1)
                elif '>' in action:
                    if action in rule:
                        print(action+" already exist in TMS.")
                        print('')
                        continue
                    else:
                        addRule(action)
            # if command is Retract then we check the condition
            elif command == 'Retract':
                if action in literal:
                    literal.remove(action)
                    total.remove(action)
                    # now check if they have derived KB, if yes then delete them too
                    removeTMS(action)
                elif action in rule:
                    literal.remove(action)
                    total.remove(action)
                    # now check if they have derived KB, if yes then delete them too
                    removeTMS(action)
                elif action not in total:
                    print(action+" does not exist in TMS.")
                    print('')
            # print the state of TMS
            print("Status of TMS: ")
            for j in total:
                print(j)
            print('')


# function to add rule when a new rule is added via TMS and to check if this rule lead to other derived literal
# and whether lead to any contradiction.
def addRule(action):
    derivedLiteral = ''
    derivedRule = []
    derivedTotal = [action]
    temp = action.strip('(').strip(')').split('>')[0]
    temp1 = action.strip('(').strip(')').split('>')[1]
    if '+' in temp:
        temp2 = temp.strip('+')[0]
        temp3 = temp.strip('+')[1]
        if temp2 in literal:
            derivedTotal.append(temp1 + ":{" + temp2 + "," + action + "}")
            derivedRule.append([temp1, [temp2, action]])
            derivedLiteral = temp1
        elif temp3 in literal:
            derivedTotal.append(temp1 + ":{" + temp3 + "," + action + "}")
            derivedRule.append([temp1, [temp3, action]])
            derivedLiteral = temp1
    elif '*' in temp:
        temp2 = temp.strip('*')[0]
        temp3 = temp.strip('*')[1]
        if temp2 in literal and temp3 in literal:
            derivedTotal.append(temp1+":{"+temp2+","+temp3+"," + action + "}")
            derivedRule.append([temp1, [temp2, temp3, action]])
            derivedLiteral = temp1
    elif temp in literal:
        derivedTotal.append(temp1 + ":{" + temp + "," + action + "}")
        derivedRule.append([temp1, [temp, action]])
        derivedLiteral = temp1
    if len(derivedRule) > 0:
        flag1 = True
        flag1 = addLiteral(derivedLiteral, flag1)
        if flag1:
            for i in derivedRule:
                derived.append(i)
            for i in derivedLiteral:
                literal.append(i)
            for i in derivedTotal:
                total.append(i)
        else:
            print("Adding "+action+" leads to contradiction.")
    else:
        total.append(action)
        rule.append(action)


# This function add the new literal as well as check if we can derive new literal using existing rules or
# update then , and will only add if no contradiction occurs.
def addLiteral(action, flag1):
    # derivedLiteral and derivedRule list are used to temporarily store the derived literal and rule to
    # check if it do not lead to any contradiction, if not add to the total, literal and derived list
    # else delete added action also with these values.
    derivedLiteral = [action]
    derivedRule = []
    derivedTotal = [action]
    #  check if a literal can be derived from the input literal
    if '-'+action in literal:
        print("Contradiction. " + action + ', -' + action)
        return False
    elif action[1:] in literal:
        print("Contradiction." + action + ', ' + action[1:])
        return False
    else:
        count = 0
        # loop will run until it check for all the added or derived literals
        # if a new literal is found it will be added to derivedLiteral list and while loop will run one more
        # time else will break when condition becomes false.
        while count < len(derivedLiteral):
            for line in rule:
                if len(derivedLiteral) > 0:
                    tempD = line.split('>')[0]
                    tempD1 = line.split('>')[1]            # tempD & tempD1 to check potential derived literals
                    # if rule is of type A>B
                    if tempD == derivedLiteral[count]:
                        flag = True
                        flag = checkValidity(flag, derivedLiteral[count], tempD1)
                        if flag:
                            derivedTotal.append(tempD1 + ":{" + tempD + "," + line + "}")
                            derivedLiteral.append(tempD1)
                            derivedRule.append([tempD1, [tempD, line]])
                        else:
                            derivedRule = []
                            derivedTotal = []
                            derivedLiteral = []
                    # if + is given in the tempD which is A+B part in A+B>C and A or B is action then
                    # C literal can be added
                    elif '+' in tempD:
                        tempD3 = tempD.split("+")[0].strip('(')
                        tempD4 = tempD.split("+")[1].strip(')')
                        # if temp3 is action
                        if tempD3 == derivedLiteral[count]:
                            flag = True
                            flag = checkValidity(flag, derivedLiteral[count], tempD1)
                            if flag:
                                derivedTotal.append(tempD1 + ":{" + tempD3 + "," + line + "}")
                                derivedLiteral.append(tempD1)
                                derivedRule.append([tempD1, [tempD3, line]])
                            else:
                                derivedRule = []
                                derivedTotal = []
                                derivedLiteral = []
                        elif tempD4 == derivedLiteral[count]:
                            flag = True
                            flag = checkValidity(flag, derivedLiteral[count], tempD1)
                            if flag:
                                derivedTotal.append(tempD1 + ":{" + tempD4 + "," + line + "}")
                                derivedLiteral.append(tempD1)
                                derivedRule.append([tempD1, [tempD4, line]])
                            else:
                                derivedRule = []
                                derivedTotal = []
                                derivedLiteral = []
                    # if rule is of type (A*B)>C
                    elif '*' in tempD:
                        tempD3 = tempD.split("*")[0].strip('(')
                        tempD4 = tempD.split("*")[1].strip(')')
                        if tempD3 == derivedLiteral[count] and tempD4 in literal:
                            flag = True
                            flag = checkValidity(flag, derivedLiteral[count], tempD1)
                            if flag:
                                derivedTotal.append(tempD1 + ":{" + tempD3 + "," + tempD4 + "," + line + "}")
                                derivedLiteral.append(tempD1)
                                derivedRule.append([tempD1, [tempD3, tempD4, line]])
                            else:
                                derivedRule = []
                                derivedTotal = []
                                derivedLiteral = []
                        elif tempD4 == derivedLiteral[count] and tempD3 in literal:
                            flag = True
                            flag = checkValidity(flag, derivedLiteral[count], tempD1)
                            if flag:
                                derivedTotal.append(tempD1 + ":{" + tempD4 + "," + tempD3 + "," + line + "}")
                                derivedLiteral.append(tempD1)
                                derivedRule.append([tempD1, [tempD4, tempD3, line]])
                            else:
                                derivedRule = []
                                derivedTotal = []
                                derivedLiteral = []
                    flag1 = True
                else:
                    flag1 = False
                    break
            count += 1
        # all the derived and new literals and rules are added to main lists.
        if len(derivedLiteral) > 0:
            for i in derivedTotal:
                if i.split(':')[0] not in literal:
                    total.append(i)
                    literal.append(i.split(':')[0])
                    for j in derivedRule:
                        if j[0] == i.split(':')[0]:
                            if j[1][0] == i.split(':')[1].split(',')[0].strip('{') or j[1][0] == i.split(':')[1].split(',')[1]:
                                derived.append(j)
                elif i.split(':')[0] in literal:
                    for j in derived:
                        if i[:1] == j[0]:
                            for k in range(len(total)):
                                if total[k][:1] == i[:1]:
                                    total[k] += ' , ' + i.split(':')[1]

            for i in derivedLiteral:
                if i not in literal:
                    literal.append(i)
        if len(derivedRule) > 0:
            for i in derivedRule:
                if i not in derivedRule:
                    derived.append(i)
    return flag1


# check if the negated value is present or not.
def checkValidity(flag, action, temp):
    for z in total:
        if (z[0] is not '-' and '-'+temp in z[:2]) or (z[0] is '-' and temp in z[:2]):
            return False
    return True


# remove the literal which is input with Retract command and all the literals and rules derived from it.
def removeTMS(action):
    removeLiteral = [action]
    removeDerived = []
    removeTotal = []
    count = 0
    while count < len(removeLiteral):
        for line in rule:
            tempR = line.split('>')[0]
            tempR1 = line.split('>')[1]

            # remove derived Literal details where condition was A>B
            if tempR == removeLiteral[count]:
                removeLiteral.append(tempR1)
                for line2 in derived:
                    if line2[1][0] == tempR and len(line2[1]) == 2:
                        removeDerived.append(line2)
                for line3 in total:
                    temp2 = ''
                    if ':' in line3:
                        temp = line3.split(':')[0]
                        temp1 = line3.split(':')[1]
                        temp3 = ''
                        if line3[:1] == tempR1:
                            if ' , ' not in temp1:
                                temp2 = line3
                            else:
                                temp1 = line3.split(':')[1].split(' , ')
                                for i in len(temp1):
                                    if len(temp1[i].split(',')) == 2 and temp[i].split(',')[0].strip('{') != tempR:
                                        temp3 += i
                                    elif len(temp1[i].split(',')) > 2:
                                        if temp3 == '':
                                            temp3 += i
                                        else:
                                            temp3 += ' , ' + i
                        line3 = temp + ':' + temp3
                    if len(temp2) > 0:
                        removeTotal.append(temp2)
                        temp2 = ''

            # Remove derived Literal details where condition was (A+B)>C
            elif '+' in tempR:
                tempR2 = tempR.split('+')[0].strip('(')
                tempR3 = tempR.split('+')[1].strip(')')
                # if tempR2 is action then we can remove its derivation from temp2.
                if tempR2 == removeLiteral[count]:
                    for line4 in derived:
                        if line4[0] == tempR1 and line4[1][0] == tempR2:
                            removeDerived.append(line4)
                    for line5 in total:
                        temp2 = ''
                        temp3 = ''
                        if line5[:1] == tempR1:
                            if ' , ' not in line5:
                                temp2 = line5
                            else:
                                temp1 = line5.split(':')[1].split(' , ')
                                for i in range(len(temp1)):
                                    if len(temp1[i].split(',')) == 2 and temp[i].split(',')[0].strip('{') != tempR2:
                                        temp3 += temp1[i]
                                    elif len(temp1[i].split(',')) > 2:
                                        if temp3 == '':
                                            temp3 += temp1[i]
                                        else:
                                            temp3 += ' , ' + temp1[i]
                        line3 = temp + ':' + temp3
                        if len(temp2) > 0:
                            removeLiteral.append(temp2.split(':')[0])
                            removeTotal.append(temp2)
                            temp2 = ''
                elif tempR3 == removeLiteral[count]:
                    for line4 in derived:
                        if line4[0] == tempR1 and line4[1][0] == tempR3:
                            removeDerived.append(line4)
                    for line5 in range(len(total)):
                        temp2 = ''
                        temp3 = ''
                        if total[line5][:1] == tempR1:
                            if ' , ' not in total[line5]:
                                temp2 = total[line5]
                            else:
                                temp1 = total[line5].split(':')[1].split(' , ')
                                for i in range(len(temp1)):
                                    if len(temp1[i].split(',')) == 2 and temp1[i].split(',')[0].strip('{') != tempR3:
                                        temp3 += temp1[i]
                                    elif len(temp1[i].split(',')) > 2:
                                        if temp3 == '':
                                            temp3 += temp1[i]
                                        else:
                                            temp3 += ' , ' + temp1[i]
                            total[line5] = temp + ':' + temp3
                        if len(temp2) > 0:
                            removeLiteral.append(temp2.split(':')[0])
                            removeTotal.append(temp2)
                            temp2 = ''
            # if rule of type (A*B)>C
            elif '*' in tempR:
                tempR2 = tempR.split('*')[0].strip('(')
                tempR3 = tempR.split('*')[1].strip(')')
                # if temp2 is action and temp3 in literal then we can remove its derivation from temp2.
                if tempR2 == removeLiteral[count]:
                    for line1 in derived:
                        if line1[0] == tempR1 and (line1[1][0] == tempR2 or line1[1][1] == tempR2):
                            removeDerived.append(line1)
                    for line6 in range(len(total)):
                        temp2 = ''
                        temp3 = ''
                        if total[line6].split(':')[0] == tempR1:
                            if ' , ' not in total[line6]:
                                temp2 = total[line6]
                            else:
                                temp1 = total[line6].split(':')[1].split(' , ')
                                for i in range(len(temp1)):
                                    if len(temp1[i].split(',')) == 3 and (temp1[i].split(',')[0].strip('{') != tempR2 or temp1[i].split(',')[1] != tempR2):
                                        temp3 += temp1[i]
                                    elif len(temp1[i].split(',')) != 3:
                                        if temp3 == '':
                                            temp3 += temp1[i]
                                        else:
                                            temp3 += ' , ' + temp1[i]
                            total[line6] = temp + ':' + temp3
                        if len(temp2) > 0:
                            removeLiteral.append(temp2.split(':')[0])
                            if temp2 in total:
                                total.remove(temp2)
                                temp2 = ''
                elif tempR3 == removeLiteral[count]:
                    for line1 in derived:
                        if line1[0] == tempR1 and (line1[1][0] == tempR3 or line1[1][1] == tempR3):
                            removeDerived.append(line1)
                    for line6 in range(len(total)):
                        temp2 = ''
                        temp3 = ''
                        if total[line6][:1] == tempR1:
                            if ' , ' not in total[line6]:
                                temp2 = total[line6]
                            else:
                                temp1 = total[line6].split(':')[1].split(' , ')
                                for i in range(len(temp1)):
                                    if len(temp1[i].split(',')) == 3 and (temp1[i].split(',')[0].strip('{') != tempR3 or temp1[i].split(',')[1] != tempR3):
                                        temp3 += temp1[i]
                                    elif len(temp1[i].split(',')) != 3:
                                        if temp3 == '':
                                            temp3 += temp1[i]
                                        else:
                                            temp3 += ' , ' + temp1[i]
                            total[line6] = temp + ':' + temp3
                        if len(temp2) > 0:
                            removeLiteral.append(temp2.split(':')[0])
                            if temp2 in total:
                                total.remove(temp2)
                                temp2 = ''
        count += 1
    for j in removeDerived:
        if j in derived:
            derived.remove(j)
    for i in removeLiteral:
        if i in literal:
            if i not in (j[0] for j in derived):
                literal.remove(i)
    for i in removeTotal:
        if i in total:
            total.remove(i)


# calling main function
__main__()
