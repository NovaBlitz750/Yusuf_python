books=["Harry Potter", "Percy Jackson", "Atomic Habits", "Fluent forever", "The Christmas Pig", "The Wild Robot"]
copies=[9,2,5,1,5,6]
lib={book: count for book, count in zip(books, copies)}
print("Library Stock:",lib )
availableb=[book for book in books if lib[book]>0]
print("Books available:",availableb)
choose=input("What book do you want to borrow")
if choose not in lib or lib[choose]==0:
    print(choose,"isnt available")
    exit()
late=[5,7,2,6,8,7]
extra=int(input("Enter the extra fee to add to every book: "))
updated_fees = list(map(lambda fee: fee + extra,late))
print("Updated Late Fees:", updated_fees)
b_index=books.index(choose)
choose_fee= updated_fees[b_index]
print("Late fee for", choose_fee, "after update:", choose_fee)
lib[choose] = lib[choose] - 1
print(choose, "borrowed! Remaining copies:", lib[choose])
print("===== LIBRARY BOOK AVAILABILITY CHECKER =====")
print("Book Borrowed:", choose)
print("Late Fee:", choose_fee)
print("Updated Library Stock:", lib)