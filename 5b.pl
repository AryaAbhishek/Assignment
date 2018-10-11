/*Following are the facts.*/

edge(landVehicle,ako,vehicle).
edge(airplane,ako,vehicle).
edge(train,ako,landVehicle).
edge(car,ako,landVehicle).
edge(airForceOne,isa,airplane).
edge(carolinian,isa,train).
edge(silverbullet,isa,car).
edge(lightning,isa,car).

/*Following are the rules to determine the relationship between any to input nodes.*/

rel(X,Y,Z):-
    edge(X,Y,Z).
rel(X,Y,Z):-
    edge(X,A,B),
    rel(B,Y,Z).

/*Here
X- SourceNode
Y- RelationshipType
Z- DestinationNode
A- Singlton Variable to check wether there any relationship (isa or ako) between X and any other node B.
B- is any node which connects Node X and Z via any relationship.*/
