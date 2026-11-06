def prime1(no):
    prime=[True for i in range(no+1)]
    p=2
    while p*p<=no:
        if prime[p]==True:
            for i in range(p*p,no+1,p):
                prime[i]=False
        p+=1
    for p in range(2,no+1):
        if prime[p]==True:
            print(p)
no=int(input("Enter a number "))
print("The folloing prime numbers are smaller than or equal to",no)
prime1(no)