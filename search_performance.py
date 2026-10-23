scores=[3,6,4,5,4,1,8,0]
target=int(input("Enter a number to search for"))
steps=0
for score in scores:
    steps+=1
    if score==target:
        break
print(" target =", target, " found at position", steps, " checks =", steps)
mid=len(scores)//2
print(" Best: 1 check -> O(1) Average:", mid," checks -> O(n)   Yours:", steps)
print(" Best O(1) Average O(n) Worst O(n)  -> Big O = worst case =O(n).")