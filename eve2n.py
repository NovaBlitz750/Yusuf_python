no=int(input("Enter a number "))
te=0
for number in range(2, no + 1, 2):
    te+=no
print(f"The sum of all even numbers from 0 to {no} is {te}")