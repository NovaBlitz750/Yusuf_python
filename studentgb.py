total=0
avg=0
high=0
low=0
stu={"Divyansh":93,
     "Evan":62,
     "Mustafa":84,
     "Ali":34,
     "Dhruv":79,
     "Vishesh":90}
for i in stu.values():
    total+=i
avg=total/6
low=min(stu.values())
high=max(stu.values())
print("Average score of class was",avg)
print("Highest scorer was Divyansh with a score of", high)
print("Lowest scorer was Ali with a score of", low)
search=input("Which student's result would you like to search for?").strip().capitalize()
while True:
    if search in stu:
        print("Marks of", search,"is",stu.get(search))
    else:
        print("Please try again,", search,"was not found in the students list")
