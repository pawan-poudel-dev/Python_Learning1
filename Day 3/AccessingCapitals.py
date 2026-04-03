country_capitals = {
  "Germany": "Berlin", 
  "Canada": "Ottawa", 
  "England": "London"
}

# access the value of keys
print(country_capitals["Germany"])    # Output: Berlin
print(country_capitals["England"])    # Output: London
country_capitals["Italy"]="Rome"
print(country_capitals)
country_capitals["Nepal"]="Kathmandu"
print(country_capitals)
#removing Dictionary 
del country_capitals["Canada"]
print(country_capitals)
country_capitals.pop("England")
print(country_capitals)
country_capitals.clear()
print(country_capitals)