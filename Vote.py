party1 = 0
party2 = 0
i = 10
while i > 0:
    vote1 = input("Who would you like to vote for? party1 or party2? ").strip()
    if vote1 == "party1":
        party1 = party1 + 1
        print("party1 now has", party1, "votes")
    else:
        party2 = party2 + 1
        print("party2 now has", party2, "votes")
    i = i - 1
if party1>party2:
    print("party1 wins the vote!")
    mkfv = input("Press enter to exit")
elif party1==party2:
    print("Its a draw!")
    mkfv = input("Press enter to exit")
else:
    print("party2 wins the vote!")
    mkfv = input("Press enter to exit")
    
   