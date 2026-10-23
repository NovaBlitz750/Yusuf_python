num=int(input("Enter a number"))
temp=num
sum=0
while temp>0:
    digit= temp%10
    sum=sum+(digit**3)
    temp=temp//10
if sum==num:
    print(num, "is an armstrong value")
else:
    print(num, "isn't an armstrong value")