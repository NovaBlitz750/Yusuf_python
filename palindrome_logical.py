no=int(input("Enter a number to check if its palindorme or not "))

original_no=no
reversed_no=0

while no>0: 
    digit=no%10
    reversed_no=reversed_no*10+digit
    no//=10

if original_no== reversed_no:
    print(f"{original_no} is a palindrome")
else:
    print(f"{original_no} isn't a palindrome")