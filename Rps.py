import random
p=0
cp=0
options = ["rock", "paper", "scissors"]
r=int(input("How many rounds would you like to play?"))
while r>0:
    kf = input("Rock! Paper! Scissors! Shoot! ").strip().lower()
    
    if kf not in options:
        print("Invalid input, try again")
        continue
    
    computer_pick = random.choice(options)
    print("Computer picked", computer_pick)
    
    if kf == computer_pick:
        print("It's a draw!")
        r-=1
    elif kf == "rock" and computer_pick == "paper":
        print("Computer wins!")
        cp+=1
        r-=1
    elif kf == "rock" and computer_pick == "scissors":
        print("You win!")
        p+=1
        r-=1
    elif kf == "paper" and computer_pick == "rock":
        print("You win!")
        p+=1
        r-=1
    elif kf == "paper" and computer_pick == "scissors":
        print("Computer wins!")
        cp+=1
        r-=1
    elif kf == "scissors" and computer_pick == "rock":
        print("Computer wins!")
        cp+=1
        r-=1
    elif kf == "scissors" and computer_pick == "paper":
        print("You win!")
        p+=1
        r-=1
if r==0 and cp>p:
    print("Computer has", cp, "points, and you have", p, "points, so computer wins by", cp-p, "points!")
    by=input("GGs")
elif cp==p:
    print("Its a draw!")
    byee=input("GGs")
else:
    print("Computer has", cp, "points, and you have", p, "points, so you win by", p-cp, "points!")
    bye=input("GGs")