/*Following are the facts.*/

edge(landVehicle,ako,vehicle).
edge(airplane,ako,vehicle).
edge(train,ako,landVehicle).
edge(car,ako,landVehicle).
edge(airForceOne,isa,airplane).
edge(carolinian,isa,train).
edge(silverbullet,isa,car).
edge(lightning,isa,car).
property(car,color,silver).
property(lightning,color,white).
property(train,travel,track).
property(airplane,travel,air).
property(landVehicle,travel,land).

/*Following are the rules to determine the relationship between any to input nodes.*/

rel(X,Y,Z):-
    edge(X,Y,Z).
rel(X,Y,Z):-
    edge(X,A,B),
    rel(B,Y,Z).

/* Here
X- SourceNode
Y- RelationshipType
Z- DestinationNode
A- Singlton Variable to check wether there any relationship (isa or ako) between X and any other node B.
B- is any node which connects Node X and Z via any relationship.*/

checkProperty(K,L,M):-
    property(K,L,M).
checkProperty(K,L,M):-
    edge(K,N,O),
    checkProperty(O,L,M),
    \+ property(K,L,_).

/*Here
K - Node
L - Travel/Color
M - Land/Track/Air/White/Silver
N - Singlton variable to get the relationshiptype between 'K'and node 'O' which has the property 'L' with Value 'M'
O - An variable which has relationship with node 'K' and also have the
property 'L' with value 'M'.
*/
