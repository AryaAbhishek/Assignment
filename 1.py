
import re
import sys
import math

searchType,srcCity,destCity = sys.argv[1].lower(),sys.argv[2],sys.argv[3]    #taking values from command line
data=open('roads.txt')		# read roads.txt file
input=[]
for i in data:					# remove unnecessary \n and \t and store in input list 
	i=i.strip('\n')
	i=i.strip('\t')
	input.append(i)
	
graph,city,cityDistance,a = [],[],{},0
pettern = re.compile('^[a-z]|[A-Z]')  # defined pattern to match only required data

# now store all cities and their coordinates in graph list
for f in input:
	if pettern.match(f) and 'Roads' not in f:
		graph.append(f.split(','))
	elif 'Roads' in f:
		break

# store all the srcCity, destCity and their distance in city list
for f in input:
	if 'Roads' in f:
		a=1
	elif a==1 and pettern.match(f):
		city.append(f.split(','))

graph=dict([(a.strip(),[float(b.strip()),float(c.strip())]) for a,b,c in graph])  #removing white spaces in graph list

for i in city:																	# putting values from city to cityDistance by converting list into 
	if i[0].strip() in cityDistance:											# dictionary of list of lists
		cityDistance[i[0].strip()].append([i[1].strip(),int(i[2].strip())])
	else:
		cityDistance[i[0].strip()]=[[i[1].strip(),int(i[2].strip())]]
	if i[1].strip() in cityDistance:
		cityDistance[i[1].strip()].append([i[0].strip(),int(i[2].strip())])
	else:
		cityDistance[i[1].strip()]=[[i[0].strip(),int(i[2].strip())]]

# variable required for bfs,dfs and astar 
nodeExpanded,solution=[],[]
lengthOfSolution = 0

#Heuristic function to calculate straight distance between start and end city values given in heuristic function 
def heuristic(start, end):
	Lat1=graph[start][0]
	Lat2=graph[end][0]
	Long1=graph[start][1]
	Long2=graph[end][1]
	return math.sqrt((69.5 * (Lat1 - Lat2)) ** 2 + (69.5 * math.cos((Lat1 + Lat2)/360 * math.pi) * (Long1 - Long2)) ** 2)

def searchUSA(searchType, srcCity, destCity):
	if searchType=='bfs':													#start bfs algorithm
		for i in cityDistance:						#sorting the cityDistance dictionary's values in ascending order
			cityDistance[i].sort()
		expand=[srcCity]				#list to store the child nodes
		while len(expand) !=0:
			traversed=expand.pop(0)
			if traversed==destCity:			# if srcCity is found, break out of the while loop
				nodeExpanded.append(traversed)
				break
			elif traversed not in nodeExpanded and traversed in cityDistance.keys() :
				for i in cityDistance[traversed]:		#loop to add the child of current node in expand list which are yet to be traversed
					if i[0] not in nodeExpanded:
						expand.append(i[0])
			nodeExpanded.append(traversed)
		node=destCity
		length=1
		while node !=srcCity:						# build solution path and length of solution path
			solution.append(node)
			for i in cityDistance[solution[-1]]:
				if i[0] in nodeExpanded[:nodeExpanded.index(solution[-1])]:
					node = i[0]
					length=length+1
		solution.append(srcCity)
		solution.reverse()		
		lengthOfSolution=length												#end bfs algorithm
	
	#DFS Algorithm	
	elif searchType=='dfs':													#start dfs algorithm
		for i in cityDistance:
			cityDistance[i].reverse()				# reverse dictionary values to use expand list as stack so we can get cities alphabetically
		expand=[srcCity]
		while len(expand) !=0:
			traversed=expand.pop(-1)
			if traversed==destCity:				#if destCity is found, save it and break out of while loop
				nodeExpanded.append(traversed)
				break
			elif traversed not in nodeExpanded and traversed in cityDistance.keys() :
				child=[]
				for i in cityDistance[traversed]:			#sort and reverse each value of cityDistance[traversed] to put them in expand 
					child.append(i[0])						#and pop them alphabetically
					child.sort()
					child.reverse()
				for i in child:								#add chile to expand if yet to be traversed
					if i not in nodeExpanded:
						expand.append(i)
			if traversed not in nodeExpanded:				#append traversed to nodeExpanded if not in nodeExpanded
				nodeExpanded.append(traversed)									
		node=destCity
		length=1
		for i in nodeExpanded[nodeExpanded.index(destCity)-1::-1]:			#Building Solution path 
			if node not in solution:
				solution.append(node)
			for j in cityDistance[i]:
				if solution[-1]==j[0] :
					if i not in solution:
						node = i
						length+=1
					break
		solution.append(srcCity)
		solution.reverse()		
		lengthOfSolution=length											#end dfs algorithm
	
	#A* algorithm
	elif searchType=='astar':					#start of astar algorithm
		totalCost={}			#totlCOst -- gCost + heuristic
		gCost={}				#total cost till a perticular node --gCost(a,c)= gCost(a,b)+gCost(b,c)
		gCost[srcCity]=0
		expand=[srcCity]		#child cities list
		totalCost[srcCity]=heuristic(srcCity,destCity)
		traversed=expand[0]
		sol=[]
		nodeExpanded.append(srcCity)
		length=1
		while len(expand)>0:
			for i in range(len(expand)):		#selecting the child with minimum totalCost
				if i==0:
					traversed=expand[0]
				elif i !=0 and len(expand)>1:
					if totalCost[expand[i]]<totalCost[traversed]:
						traversed=expand[i]
					else:
						traversed=traversed
			if traversed==destCity:			#if found destCity,break out of the while loop
				break
			expand.remove(traversed)			#remove the traversed node
			sol.append(traversed)			#add traversed node to the solution path
			#length+=1
			for i in cityDistance[traversed]:		#if child is in solution then skip current iteration and continue with loop
				if i[0] in sol:
					continue
				if i[0] not in expand:				#if child not in expand list then add it
					expand.append(i[0])
				
				cost=gCost[traversed]+i[1]			# total cost till traversed + cost from traversed till 'i' node
				#if cost>=traversed[1]:
				#	continue
				nodeExpanded.append(i[0])			# add the child in nodeExpanded list
				gCost[i[0]]=cost					#cost is the total path distance from srcCity to 'i' city
				totalCost[i[0]]=gCost[i[0]]+heuristic(i[0],destCity) #total cost from srcCity till 'i' city + heuristic(i,destCity)
		sol.append(destCity)
		solution.append(destCity)
		for i in sol[::-1]:
			for j in cityDistance[i]:
				if solution[-1]==j[0]:
					if i not in solution:
						solution.append(i)
						length+=1
					break
		solution.reverse()
		lengthOfSolution=length
		print('The Cost of path: ',totalCost[destCity])
	print('List of expanded nodes: ',nodeExpanded)
	print('Number of expanded nodes: ',len(nodeExpanded))
	print('solution path: ',solution)
	print('Total Length of solution path: ',lengthOfSolution)
	
searchUSA(searchType, srcCity, destCity)			#calling searchUSA function