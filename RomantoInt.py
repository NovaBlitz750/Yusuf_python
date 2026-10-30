no=input("Enter a Roman number ").strip().upper()
values={"V":5, "I":1, "X":10, "L":50, "C":100, "D":500, "M":1000}
num=0
for i in range (len(no)):
    if i+1<len(no) and values[no[i]]< values[no[i+1]]:
        num-=values[no[i]]
    else:
        num+=values[no[i]]
print(num)