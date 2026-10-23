password="abc123"
answer=input("Enter the password")
if answer==password:
	print("Correct password")
	Correct=input("You have been verified!")
else:
	print("No, that is the wrong password, try again")
	answer2=input("Try entering the password again")
	if answer2==password:
	    print("Correct password")
	    Correct2=input("You have been verified!")
	else:
	    print("That is incorrect again")
	    lock=input("You have been locked out, press enter to exit")

