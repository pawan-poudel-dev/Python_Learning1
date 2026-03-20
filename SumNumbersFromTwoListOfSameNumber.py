#list1[1,2,3,4,5,6]
#list2[1,2,3,4,5,6]
list1 = [1,2,3,4,5,6]
list2 = [1,2,3,4,5,6]
#using the for each loop
#print in list 
#using resukt.append{list1[i]+list2[j]}
sum =0
list_3 = []
for i in range(len(list1)):
 list_3.append(list1[i]+list2[i])
print(list_3)
            #print("the sum of the numbers from two list is ",list_3)
"""for i in list1:
    for j in list2:

        if i==j:
            sum = i+j
            list_3.append(sum)
print("the sum of the numbers from two list is ",list_3)"""
