guess= input(" At n = 1000, O(n^2) takes how many steps? ")
for n in [10, 100, 1000]:
    input("n = "+ str(n) + " Press Enter ")
    print(" O(n) =", n, "O (n^2) =",  n*n)

print(" Your guess:", guess)
input("Full ladder at n=1000. Press Enter")
print(" O(1)=1  O(log n)=10 O(n)=1000 O(n^2)=1,000,000")P