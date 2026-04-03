maths= {"pawan":18,"poudel":19.009}
'''print(maths["pawan"])
maths["pawan"]=20
print(maths)
del( maths["pawan"])
print(maths)'''
#iterating through loop
'''for key ,value in maths.items():
    print(key,value)'''
for key in maths.keys():
    print(key)
    for value in maths.values():
        print(value)

