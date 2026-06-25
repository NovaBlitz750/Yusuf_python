list=['abc', 'cfc','xyz', 'aba', '1221']
def count(list):
    sat=0
    list2=[]
    for i in list:
        if len(i)>1 and i[0]==i[-1]:
            sat+=1
            list2.append(i)
    print("The amount of strings in the list that satisy the conditions are:", sat)
    print("Those strings are", list2)
count(list)