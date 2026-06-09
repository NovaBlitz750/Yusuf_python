def cube(no):
    return no**3
def div_check(no):
    if no%3==0:
        return cube(no)
    else:
        return "Since", no,"isnt divisible by 3, cube won't be calculated in this program"
no=int(input("Enter a number"))
print("The cube of",no,"is",div_check(no))