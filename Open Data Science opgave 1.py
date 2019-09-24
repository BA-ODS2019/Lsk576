import pandas as pd
import os
import re
import matplotlib.pyplot as plt

#Opgave 2

data = pd.read_csv(r"C:\Users\Christoffer\Desktop\CSV DATA\titanic.csv", encoding="utf-8")

data_size = data.shape

data_dimensions = data.ndim

print(data_dimensions);
#_________________________________________________


#Opgave 3

total_pop = len(data);
    
survivors = data['Survived'].sum()

print("The amount of survivors are: "+str(survivors), "out of the total population "+str(total_pop))
#_________________________________________________

average_age = data['Age'].sum()

average_age = average_age / len(data)

print('Average age is '+ str(average_age) + " years")
#_________________________________________________

median_age = data['Age'].median()

print('Median age is ' + str(median_age) + " years")
#_________________________________________________

average_price = data['Fare'].sum()

average_price = average_price / len(data)

print('Average price is '+ str(average_price) + " Dollars")
#_________________________________________________
#_________________________________________________________________


#Opgave 4

names = []

lastnames = []

for x in range(0, len(data)):
    element= data['Name'][x]
    names.append(element)

for x in range(0, len(names)):
    element = names[x].split()
    
    if len(element) == 4:
        lastnames.append(element[3])
    if len(element) == 3:
        lastnames.append(element[2])


print("Are there more of one identical element in my list? : " + str(len(lastnames) != len(set(lastnames))))
        
        
#_________________________________________________________________

#Opgave 5

table1 = pd.pivot_table(data, index=["Pclass"], values=["Survived"], margins=True)

print(table1)



    
    
    
    
    
    
    
