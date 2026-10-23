n=4
guess=input("Total points: 1+2+3+4 = ")
total=n*(n+1)//2
print("total=", total, "steps=1")
total=0
for students in range(1,n+1):
    total+=students
print("total", total,"steps=",n)
total=0
steps=0
for students in range(1,n+1):
    for point in range(1,students+1):
        total+=1
        steps+=1
print("total=",total, "steps=", steps, "your guess was:", guess)
