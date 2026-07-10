m=0
test_dict={'Codingal':3,
           'is': 2,
           'best':2,
           'for':2,
           'Coding':1}
val=int(input("Frequency of what value shall be checked in the dictionary"))
for i in test_dict.values():
    if i==val:
        m+=1
print("The number of occurences of", val,"in the dictionary is",m,"times")