tuple1=("d",8,2,"f",3)
tuple2=(3,5,2,5,3,5,)
t3=tuple2+(9,)
count=0
print(tuple1)
print(tuple2)
print(t3)
for i in range(0,len(tuple2)):
    if tuple2[i]==5:
        count+=1
    else:
        pass
print(f"tuple2 has 5 {count} many times in it")
print(tuple2.count(5))