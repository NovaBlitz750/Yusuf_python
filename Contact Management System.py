User1 = {"Name": "Faisal", "Nationality": "Indian", "Phone number": "7415000219", "Address": "Hillcrest", "Gmail": "faisal.sapsd@gmail.com"}
User2 = {"Name": "Ishrat", "Nationality": "Indian", "Phone number": "8817912070", "Address": "Hillcrest", "Gmail": "ishrat.jahan86@gmail.com"}
User3 = {"Name": "Yusuf", "Nationality": "Indian", "Phone": "No Phone Number", "Address": "Hillcrest", "Gmail": "syedyusufali.21077g@spsstudent.ac.in"}
password1 = "2013"
password2 = "Yusuf@123"
password3 = "CheekyP@rrot"
while True:
    ask = input("Enter the password for unlocking your personal info")
    if ask == password1:
        print("Correct password entered!")
        print(User1)
    elif ask == password2:
        print("Correct password entered!")
        print(User2)
    elif ask == password3:
        print("Correct password entered!")
        print(User3)
    else:
        print("Wrong password entered!")