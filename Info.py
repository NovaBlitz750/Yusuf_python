name=input("What is ur name?")
age=input("How old are u?")
address=input("Where do u live?")
password=input("What password do u want")
enter=input("Enter the password for unlocking ur personal info")
if enter==password:
    print("Correct password entered, here is ur personal info: Name:", name, "Age:", age, "Address:", address)
    done=input("Press enter to exit")
else:
    print("No, that is the wrong password, try again")
    answer2=input("Try entering the password again")
    if answer2==password:
        print("Correct password entered, here is ur personal information:Name:", name, "Age:", age, "Address:", address)
        Correct2=input("Press enter to exit")
    else:
        answer3=input("No, that is the wrong password,try again")
        if answer3==password:
            print("Correct password entered here is ur personal information:Name:", name, "Age:", age, "Address:", address)
            Correct3=input("Press enter to exit")
        else:
            print("That is incorrect again")
            lock=input("You have been locked out, press enter to exit")











    