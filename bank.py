import time
def sp(text, delay=0.05):
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()
acts={}
while True:
    sp("Welcome to the bank!")
    print("1.Withdraw amount")
    print("2.Deposit amount")
    print("3.Inquire amount")
    print("4.Create account")
    ac=int(input(""))
    if ac==4:
        name=input("Enter your full name")
        np=input("Enter your deisred password")
        balance=float(input("Starting balance"))
        with open("names.txt", "a") as file:
            file.write(name + "\n")
        acts[name]={np,balance}
        password = np   
        balance = balance 
        print("Account made!")
    elif ac==3:
        name=input("Enter your full name")
        if name in acts:
            pas=input("Enter your account password")
            if [acts]{name,np} == pas:
                print("Login successful!")
                user_account = acts[name]
                print("Your balance is:", user_account["balance"])
            else:
                print("Wrong password")
        else:
            print("User not found")
    elif ac==2:
        name=input("Enter your full name")
    if name in acts:
        pas=input("Enter your account's password")