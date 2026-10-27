scores=[1,3,5,7,9,11,15,17]
print("List:", scores)
target= int(input("Pick a number from the list: "))

low,high=0, len(scores)-1
steps=0
while low<=high:
    mid=(low+high)//2
    steps+=1
    print(" round", steps, "-> checked", scores[mid])
    if scores[mid]==target:
        break
    elif scores[mid] < target:
        low=mid+1
    else:
        high=mid-1
print(" found number", target, "at position:", steps," -> 0(log n)")
