passc = 0
symbols = "!@#$%^&*()_+-=[]{}|;':\",./<>?"
passw = input("Enter your password to check its strength: ")

for char in passw:
    if char in symbols:
        passc += 1.5
    if char.isupper():
        passc += 1
    if char.islower():
        passc += 0.5
    if char.isspace():
        passc -= 1  # spaces weaken the password
if len(passw) < 8:
    passc -= 1
if len(passw) >= 8 and len(passw) <= 19:
    passc += 1.5
if len(passw) >= 20:
    passc += 2.5

if passc <= 1:
    print("Your password is extremely weak and should be changed immediately. On a score of 1-9, here would be your password's score:", passc)
elif passc > 1 and passc < 3:
    print("Your password is weak. On a score of 1-9, here would be your password's score:", passc)
elif passc>3 and passc<=4:
    print("Your password is moderately strong. On a score of 1-9, here would be your password's score:", passc)
elif passc >= 5 and passc <= 6:
    print("Your password is very strong.On a score of 1-9, here would be your password's score:", passc )
elif passc>6:
    print("Your password is as strong as they come! On a score of 1-9, here would be your password's score:", passc)