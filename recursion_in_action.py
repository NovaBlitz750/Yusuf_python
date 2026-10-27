n=int(input("Enter n (try 3 or 5): "))

def countdown(num):
    print(" call-n =", num)
    if num>0:
        countdown(num-1)
countdown(n)
print(" calls=", n+1, "-> O(n)")
for size in [5,10,100]:
    print(" n=", size, "calls=", size+1," -> O(n)")