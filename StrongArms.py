no=int(input("Enter a Number "))
digits=len(str(no))
resultno=0
tempno=no
while tempno>0:
    digit=tempno%10
    resultno+=digit**digits
    tempno//=10
if no==resultno:
    print("It is an ARMSTRONG NUMBER")
else:
    print("It isnt an ARMSTRING NUMBER")