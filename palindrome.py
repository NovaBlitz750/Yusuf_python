inp=input("Enter anything to check if its a palindrome ")
if inp[::-1]==inp:
    print(inp," is a palindrone")
else:
    print(inp,"isnt a palindrome")