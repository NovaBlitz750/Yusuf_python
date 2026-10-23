name="Yusuf"
Age="13"
nationality="Indian"
address="Hillcrest Aurora Terese"
password="Ibu@123"
at=input("Enter the password to unlock ur info")
if at==password:
    print("Correct password entered, here is ur personal info: Name:", name, "Age:", Age, "Address:", address)
    done=input("Press enter to exit")
else:
    print("Incorrect password")
    at2=input("Try again")
    if at2==password:
                    print("Correct password entered, here is ur personal info: Name:", name, "Age:", Age, "Address:", address)
                    done2=input("Press enter to exit")
    else:
        print("Incorrect password")
        at3=input("Try again")
        if at3==password:
            print("Correct password entered, here is ur personal info: Name:", name, "Age:", Age, "Address:", address)
            ef=input("Press enter to exit")
        else:
            print("Incorrect password you have been locked out")
            bye=input("Press enter to exit")
