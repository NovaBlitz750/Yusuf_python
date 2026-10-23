amnt=int(input("Enter an amount"))
note1=(amnt//100)
note=(amnt%100)//50
note2=((amnt%100)%50)//10
print(note1, "notes of 100",note,"notes of 50 and",note2,"notes of 10")