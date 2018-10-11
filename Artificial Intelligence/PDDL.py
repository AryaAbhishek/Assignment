#!/usr/bin/env python

# Getting input from pddl.txt
file = open('pddl.txt')
graph = []
for i in file:
    graph.append(i.strip(',\n'))
plan = {}
for i in graph:
    if i[:4] == 'Init':
        plan['Init'] = i[5:len(i)-1].split(',')
    elif i[:4] == 'Goal':
        plan['Goal'] = i[5:len(i)-1].split(',')
    elif i[:6] == 'action' and 'action' not in plan.keys():
        plan['action'] = [i[7:len(i)]]
    elif i[:6] == 'action' and 'action' in plan.keys():
        plan['action'].append(i[7:len(i)])
    if i[:7] == 'PRECOND':
        plan[plan['action'][-1]] = [{i[:7]: i[8:len(i)]}]
    if i[:6] == 'EFFECT':
        plan[plan['action'][-1]].append({i[:6]: i[7:len(i)-1]})

TAction = plan['action']
States = {'S0': []}
Action = {'A0': []}
a = 0

# creating States and Action and getting Action plan

ActionState = []
Mutex = []
ShowMutex = []
StateMutex = []
ShowStateMutex = []
end = 0
while True:
    ActionState.append({})
    if a == 0:
        # Entering States starting from S0
        for i in range(len(TAction)):
            # print(plan['action'][i])
            precondition = plan[TAction[i]][0]['PRECOND'].split(',')
            # print(precondition)
            for j in precondition:
                if j in plan['Init']:
                    if j not in States['S'+str(a)]:
                        States['S'+str(a)].append(j)
                elif j[:1] == '~' and j[1:] not in plan['Init']:
                    if j[1:] not in States['S'+str(a)]:
                        States['S'+str(a)].append(j)
        for i in TAction:
            PriState = plan[i][0]['PRECOND'].split(',')
            temp = True
            for j in PriState:
                if j not in States['S'+str(a)]:
                    temp = False
                    break
            if temp:
                Action['A'+str(a)].append(i)
        for i in States['S'+str(a)]:
            Action['A'+str(a)].append('c('+i+')')
    else:
        States['S'+str(a)] = States['S'+str(a-1)]
        for i in Action['A'+str(a-1)]:
            if i[:2] == 'c(':
                if i not in ActionState[a]:
                    ActionState[a][i] = [[i[2:len(i)-1],i[2:len(i)-1]]]
                else:
                    ActionState[a][i].append([i[2:len(i)-1],i[2:len(i)-1]])
            else:
                PriState = plan[i][0]['PRECOND'].split(',')
                temp = True
                for j in PriState:
                    if j not in States['S'+str(a-1)]:
                        temp = False
                        break
                if temp:
                    AftState = plan[i][1]['EFFECT'].split(',')
                    for j in AftState:
                        if j not in States['S'+str(a)]:
                            States['S'+str(a)].append(j)
                        if j[:1] == '~' and j[1:] in PriState:
                            if i not in ActionState[a]:
                                ActionState[a][i] = [[j[1:],j]]
                            else:
                                ActionState[a][i].append([j[1:],j])
                        elif ('~'+j) in PriState:
                            if i not in ActionState[a]:
                                ActionState[a][i] = [['~'+j, j]]
                            else:
                                ActionState[a][i].append(['~'+j, j])
                        else:
                            if i not in ActionState[a]:
                                ActionState[a][i] = [[plan[i][0]['PRECOND'], plan[i][1]['EFFECT']]]
                            else:
                                ActionState[a].append([plan[i][0]['PRECOND'], plan[i][1]['EFFECT']])
        Action['A'+str(a)] = []
        for i in TAction:
            PriState = plan[i][0]['PRECOND'].split(',')
            temp = True
            # print(PriState)
            for j in PriState:
                # print("__________________"+j)
                if j not in States['S'+str(a)]:
                    temp = False
                    break
            # print(temp)
            if temp:
                Action['A'+str(a)].append(i)
                # print(Action['A'+str(a)])
        for i in States['S'+str(a)]:
            Action['A'+str(a)].append('c('+i+')')
    if end !=1:
        print("Current Action Plan Action A"+str(a)+", ActionStates are: ->")
        if len(ActionState[a]) > 0:
            for i in ActionState[a]:
                # print(ActionState[a][i])
                for j in ActionState[a][i]:
                    print(j[0]+' --> '+i + ' --> '+j[1])
        else:
            print('State S'+str(a)+' is Initial State.')
        print()
        print("Current State: S"+str(a)+" Propositions are following: ->")
        print(States['S'+str(a)])
        print()


# Mutex on Action
    ShowMutex.append([])
    for i in Action['A'+str(a)]:
        if i[:2] != 'c(':
            Before = plan[i][0]['PRECOND'].split(',')
            After = plan[i][1]['EFFECT'].split(',')
        else:
            Before = [i[2:len(i)-1]]
            After = [i[2:len(i)-1]]
        ShowMutex[a].append({i: [Before, After]})
    # print(ShowMutex[a])
    # print()

# Mutex on Action - Inconsistent Effect
    Mutex.append([])
    print("Following are the Mutexes on Action(A"+str(a)+"):-")
    # print()
    for i in range(len(ShowMutex[a])-1):
        temp = []
        previous = ''
        for j in ShowMutex[a][i]:
            previous = j
            for k in range(len(ShowMutex[a][i][j])):
                if k == 1:
                    temp = ShowMutex[a][i][j][k]
        for j in range(i+1, len(ShowMutex[a])):
            for k in ShowMutex[a][j]:
                for l in range(len(ShowMutex[a][j][k])):
                    if l == 1:
                        temp1 = ShowMutex[a][j][k][l]
                        for x in temp:
                            if '~'+x in temp1:
                                Mutex[a].append([previous, k])
                                print("Inconsistent Effect:-", previous, k)
                            elif x[1:] in temp1:
                                Mutex[a].append([previous, k])
                                print("Inconsistent Effect:-", previous, k)

    # Mutex on Action - Interference
    temp2 = []
    for i in range(len(ShowMutex[a])-1):
        temp = []
        previous = ''
        for j in ShowMutex[a][i]:
            previous = j
            for k in range(len(ShowMutex[a][i][j])):
                if k == 1:
                    temp = ShowMutex[a][i][j][k]
                    # print(temp, '-------------------------------------------------')
        for j in range(len(ShowMutex[a])):
            if j != i:
                for k in ShowMutex[a][j]:
                    for l in range(len(ShowMutex[a][j][k])):
                        if l == 0:
                            temp1 = ShowMutex[a][j][k][l]
                            # print(temp1,'+++++++++++++++++++++++++++++++++++++++')
                            for x in temp:
                                if '~'+x in temp1:
                                    if ([previous, k] not in temp2) and ([k, previous] not in temp2):
                                        temp2.append([previous, k])
                                        # print(temp2)
                                        print('Interference :- ', previous, k)
                                    if ([previous, k] not in Mutex[a]) and ([k, previous] not in Mutex[a]):
                                        Mutex[a].append([previous, k])
                                elif x[1:] in temp1:
                                    if ([previous, k] not in Mutex[a]) and ([k, previous] not in Mutex[a]):
                                        Mutex[a].append([previous, k])
                                    if ([previous, k] not in temp2) and ([k, previous] not in temp2):
                                        temp2.append([previous, k])
                                        # print(temp2)
                                        print('Interference :- ', previous, k)

    # Mutex on Action - Competing Needs
    temp2 = []
    for i in range(len(ShowMutex[a])-1):
        temp = []
        previous = ''
        for j in ShowMutex[a][i]:
            previous = j
            for k in range(len(ShowMutex[a][i][j])):
                if k == 0:
                    temp = ShowMutex[a][i][j][k]
        for j in range(i+1, len(ShowMutex[a])):
            for k in ShowMutex[a][j]:
                for l in range(len(ShowMutex[a][j][k])):
                    if l == 0:
                        temp1 = ShowMutex[a][j][k][l]
                        for x in temp:
                            if x in temp1:
                                if [previous, k] not in temp2 and [k, previous] not in temp2:
                                    temp2.append([previous, k])
                                    print("Competing Needs:- ", previous, k)
                                if [previous, k] not in Mutex[a] and [k, previous] not in Mutex[a]:
                                    Mutex[a].append([previous, k])
                            # elif x[1:] in temp1:
                            #     if [previous, k] not in Mutex[a] and [k,previous] not in Mutex[a]:
                            #         Mutex[a].append([previous, k])
                            #     if [previous, k] not in temp2 and [k, previous] not in temp2:
                            #         temp2.append([previous, k])
                            #         print("Competing Needs:- ", previous, k)
    # print('Mutex On Actions.')
    # for i in Mutex[a]:
    #     print('Action Mutex:- ', i[0], ' , ', i[1])
    print()

    # Mutex on States
    print("Following are the Mutexes on prepositions in State(S"+str(a)+"):-")
    StateMutex.append([])
    StateMutex.append([])
    if a == 0:
        print("No mutexes on this state.")
    if a > 0:
        # Negation Between States
        for i in range(len(States['S'+str(a)])-1):
            for j in range(i+1,len(States['S'+str(a)])):
                if '~'+States['S'+str(a)][i] == States['S'+str(a)][j]:
                    if [States['S'+str(a)][i], States['S'+str(a)][j]] not in StateMutex[a]:
                        print('Negation Between States:- ', States['S'+str(a)][i], States['S'+str(a)][j])
                        StateMutex[a].append([States['S'+str(a)][i], States['S'+str(a)][j]])
                elif States['S'+str(a)][i] == '~'+States['S'+str(a)][j]:
                    if [States['S'+str(a)][i], States['S'+str(a)][j]] not in StateMutex[a]:
                        print('Negation Between States:- ', States['S'+str(a)][i], States['S'+str(a)][j])
                        StateMutex[a].append([States['S'+str(a)][i], States['S'+str(a)][j]])

        # Mutex on Preposition - Inconsistent Support
        temp = []
        for i in range(len(States['S'+str(a)])):
            tempAction = []
            mutexAction = []
            for j in ActionState[a]:
                for k in ActionState[a][j]:
                    if States['S'+str(a)][i] == k[1]:
                        if ActionState[a] not in tempAction:
                            tempAction.append(j)
            # print(tempAction)
            for j in tempAction:
                for k in Mutex[a-1]:
                    if j == k[0] and k[1] not in mutexAction:
                        mutexAction.append(k[1])
                    elif j == k[1] and k[0] not in mutexAction:
                        mutexAction.append(k[0])
            mutexProposition = []
            for j in mutexAction:
                for k in ActionState[a][j]:
                    if k[1] not in mutexProposition and k[1] != States['S'+str(a)][i]:
                        mutexProposition.append(k[1])
            # print(mutexProposition)
            # if States['S'+str(a)][i] == 'Dinner':
            #     print(mutexProposition)
            #     print(mutexAction)
            for j in mutexProposition:
                z = 0
                for k in ActionState[a]:
                    for l in ActionState[a][k]:
                        if l[1] == j:
                            for m in tempAction:
                                if [k, m] not in Mutex[a] and [m, k] not in Mutex[a]:
                                    z = 0
                                    break
                                z += 1
                if z > 0:
                    if [States['S'+str(a)][i], j] not in temp and [j, States['S'+str(a)][i]] not in temp:
                        temp.append([States['S'+str(a)][i], j])
                        print("Inconsistent Support:- ", States['S'+str(a)][i], j)
                if [States['S'+str(a)][i], j] not in StateMutex[a] and [j, States['S'+str(a)][i]] not in StateMutex[a]:
                    StateMutex[a].append([States['S'+str(a)][i], j])

    print()
    a += 1

# Check Weather we have received the goal state if yes, Try to look for solution path.
    for i in plan['Goal']:
        if i in States['S'+str(a-1)]:
            stop = True
        else:
            stop = False
            break
    if stop:
        start = ''
        for i in plan['Goal']:
            if '~'+i not in States['S'+str(0)] and i[1:] not in States['S'+str(0)]:
                start = i
        previousNode = []
        previousAction = []
        for i in (a, 0, -1):
            if i == a:
                for j in ActionState[a-1]:
                    if start in ActionState[a-1][j][0][1] and start not in ActionState[a-1][j][0][0].split(','):
                        previousNode.append(ActionState[a-1][j][0][0].split(','))
                        previousAction.append(j)
                # print(ActionState[a-1][j])
                #print(previousNode)
                # for k in previousNode:
                #     if k not in States[a-1]:

            # else:
            #
            #     for j in previousNode:

                print()
        end += 1
    if end == 2:
        #print("No, Possible path found in 2 search after getting to Goal state.")
        break
