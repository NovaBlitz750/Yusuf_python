print("1.Bike")
print("2.Car")
ride=int(input("Choose your ride"))
if ride==1:
    print("1.Scooty")
    print("2.Motorbike")
    bike=int(input("Choose your 2 wheeler ride"))
    if bike==1:
        print(" Scooty selected successfully!")
    elif bike==2:
        print("Motorbike selcted successfully!")
    else:
        print("Please select a valid option")
elif ride==2:
    print("SUV")
    print("Sedan")
    car=int(input("Select which type of car you want to ride in"))
    if car==1:
        print("SUV selected successfully!")
    elif car==2:
        print("Sedan selected successfully!")
    else:
        print("Please select a valid option ")
else:
    print("Please select a valid option")