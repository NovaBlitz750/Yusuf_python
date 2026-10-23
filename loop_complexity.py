n=int(input("Enter any number"))
for i in range(n):
     pass
print(" n =", n, "steps=", n, "-> O(n) linear time")
for i in range(n):
     for j in range(n):
        pass
print(" n =", n, " steps=", n*n, "  -> O(n^2) quadratic time")