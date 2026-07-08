intset={1,2,3,4,5,6}
mixset={1,"hello",3}
mixintset={9,5,3,6,3,8,5,10}
c= intset.intersection(mixintset)
d= intset.union(mixset)
e= mixintset.difference(intset)
print(intset)
print(mixset)
print(mixintset)
print(c)
print(d)
print(e)