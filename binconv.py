no=float(input("Enter a decimal number"))
temp=no
binary = ""
while no>0:
    rem= no%2
    binary= str(rem)+binary
    no= no//2
print(f"The binary form of {temp} is {binary}")