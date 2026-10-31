seats=[12, 22, 41, 43, 43, 44, 54, 71, 75, 76, 87, 87, 88]
target=int(input("Enter ur ticket no: "))

left=0
right=len(seats)-1

steps=0

if target in seats:
    while left<=right:
        steps+=1
        mid=(left+right)//2
        print("Round:", steps, "checked for:", seats[mid])
        if seats[mid]==target:
            break
        elif seats[mid]<target:
            left=mid+1
        else:
            right=mid-1
    print("Ticket: #",target, "found at index", mid, "in", steps, "rounds")
else: 
    print("Ticket not found in list,\nPlease enter a valid input")