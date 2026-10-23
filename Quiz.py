points = 0
answer1 = "Moscow"
answer2 = "Canberra"
ans3 = "India"
ans4 = "Wellington"
ans5 = "7"
ans6 = "Water"
ans7 = "Asia"
ans8 = "Paris"
ans9 = "United Nations"
ans10 = "Italy"
ans11 = "Nirobi"
ans12 = "193"
ans13 = "Google"
ans14 = "Oslo"
ans15 = "Helsinki"
def correct_answer():
    global points
    points += 1
    print("Correct answer!")
    print("Good job!")
def wrong_answer():
    print("Oops, that was the wrong answer")
def ez_dif():
    print("Answer the following questions in one word. Good Luck!")
    
    q6 = input("70% of the Earth is made up of which material? ")
    if q6.strip().capitalize() == ans6:
        correct_answer()
    else:
        wrong_answer()
    q7 = input("What is the largest continent of the world? ")
    if q7.strip().capitalize() == ans7:
        correct_answer()
    else:
        wrong_answer()
    q8 = input("What is the capital of France? ")
    if q8.strip().capitalize() == ans8:
        correct_answer()
    else:
        wrong_answer()
    q9 = input("What is the full form of UN? ")
    if q9.strip().title() == ans9:
        correct_answer()
    else:
        wrong_answer()
    q10 = input("Pizza is originated in which country? ")
    if q10.strip().capitalize() == ans10:
        correct_answer()
    else:
        wrong_answer()
def med_dif():
    print("\nAnswer the following questions in one word. Good Luck!")
    
    q1 = input("What is the capital of Russia? ")
    if q1.strip().capitalize() == answer1:
        correct_answer()
    else:
        wrong_answer()
    q2 = input("What is the capital of Australia? ")
    if q2.strip().capitalize() == answer2:
        correct_answer()
    else:
        wrong_answer()
    q3 = input("What is the most populated country in 2026? ")
    if q3.strip().capitalize() == ans3:
        correct_answer()
    else:
        wrong_answer()
    q4 = input("What is the capital of New Zealand? ")
    if q4.strip().capitalize() == ans4:
        correct_answer()
    else:
        wrong_answer()
    q5 = input("How many continents are there in the world? ")
    if q5.strip() == ans5:
        correct_answer()
    else:
        wrong_answer()
def har_dif():
    print("\nAnswer the following questions in one word. Good Luck!")
    
    q11 = input("What is the capital of Kenya? ")
    if q11.strip().capitalize() == ans11:
        correct_answer()
    else:
        wrong_answer()
    q12 = input("How many countries are there in the UN? ")
    if q12.strip() == ans12:
        correct_answer()
    else:
        wrong_answer()
    q13 = input("Jules is an asynchronous coding agent released by which company? ")
    if q13.strip().capitalize() == ans13:
        correct_answer()
    else:
        wrong_answer()
    q14 = input("What is the capital of Norway? ")
    if q14.strip().capitalize() == ans14:
        correct_answer()
    else:
        wrong_answer()
    q15 = input("What is the capital of Finland? ")
    if q15.strip().capitalize() == ans15:
        correct_answer()
    else:
        wrong_answer()
while True:
    points = 0
    print("Welcome to the quiz!")
    dif = input("Choose a difficulty level (Easy, Medium, Hard): ").strip().capitalize()
    if dif == "Easy":
        ez_dif()
    elif dif == "Medium":
        med_dif()
    elif dif == "Hard":
        har_dif()
    else:
        print("Invalid difficulty selected.")
    print("\nThat's the end of the quiz!")
    print(f"Your score was {points} points!")
    bye = input("Press Enter to exit!")
    break