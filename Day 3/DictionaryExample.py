#creating a key Value pair 
'''country_capitals = {"Gemany":"Berlin",
                    "Canada" :"Ottawa",
                    "England":"London"}
#printing the dictionary
print(country_capitals)'''

#calid dictionary
#integer as a key 
my_dict ={1:"one",2:"two",3:"Three"}
print(my_dict)#tuple as key this is a valid 
my_Dictionary = {(1,2):"One two",3:"Three"}
print(my_Dictionary)
#invalid dictionary
#we get error using a list as a key is not allowed 
my_dict2 ={1:"Hello",[1,2]:"Hello Hi"}
print(my_dict2)
#valid dictionary
    #String as a key , list as a value 
my_dict3 ={"USA":["Chicago","California","New York"]}
print(my_dict)