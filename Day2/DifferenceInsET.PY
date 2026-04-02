#first set 
A = {2,3,4,5,11}
B ={3,4,5,6,7,8,9,1,2,3}
#first we have to find the union of set
# It can be  done in two ways using union(),|
c = A.union(B)
F= A|B
print("Union is using |:",F)
print("The union of the given set is:",c)
d =A.intersection(B)
e= A&B
print("INtersection is using &", e)
print("INtersection using:  ",d)
# the difference of the two sets are 
#this can be done  in two ways using - operator and difference() inbuilt function
j = A-B
print("USING - OPERATOR:", j)
K = A.difference(B)
print("Using difference() inbuilt fucntion:",K)
