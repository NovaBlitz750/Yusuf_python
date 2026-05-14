a=5
b=2
c=6
d=10
e=a**b%d
print(e)
f=int(input("Enter a number"))
g=int(input("Enter another number"))
if f%g==0:
    print(f, "is divisible by", g, "The answer of", f, "divided by", g, "will be", f%g)
else:
    print("They are not completely divisble by each other")
v=10
y=20
z=30
x=v+y+z
avg=x//3
print("The average speed of the 3 cyclists is",avg)
if v<avg:
    print("The first cyclist is riding slower than the average speed")
elif y<avg:
    print("The second cyclist is riding slower than the average speed")
elif z<avg:
    print("The third cyclist is riding slower than the average speed")
else:
    print("None of the cyclists are riding slower than the average speed")
no1=int(input("Enter a number"))
no=int(input("Enter another number"))
q=no1
r=no
no1=r
no2=q
print(r,q)