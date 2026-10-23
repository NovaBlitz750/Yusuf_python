# PART 1: Create the library's book names and available copy counts
books = ["matilda", "harry potter", "wonder", "the jungle book", "charlie"]
copy_counts = [4, 0, 6, 3, 2]

# PART 2: Pair books with copy counts into a dictionary
library = {book: count for book, count in zip(books, copy_counts)}
print("Full Library Stock:", library)

# PART 3: Filter only the books that are available
available_books = [book for book in books if library[book] > 0]
print("Books Available:", available_books)

# PART 4: Ask the reader which book they want to borrow
chosen_book = input("Which book do you want to borrow? ")

# PART 5: Stop the checker early if the chosen book is not available
if chosen_book not in library or library[chosen_book] == 0:
    print(chosen_book, "is not available! Stopping the checker.")
    exit()

# PART 6: Create late fees and ask for an extra fee amount
late_fees = [5, 8, 4, 6, 7]
extra_fee = int(input("Enter the extra library fee to add to every book: "))

# PART 7: Apply the extra fee to every late fee using map()
updated_fees = list(map(lambda fee: fee + extra_fee, late_fees))
print("Updated Late Fees:", updated_fees)

# PART 8: Find the updated fee of the chosen book
book_index = books.index(chosen_book)
chosen_fee = updated_fees[book_index]
print("Late fee for", chosen_book, "after update:", chosen_fee)

# PART 9: Reduce the copy count after borrowing
library[chosen_book] = library[chosen_book] - 1
print(chosen_book, "borrowed! Remaining copies:", library[chosen_book])

# PART 10: Print the final library summary
print("")
print("===== LIBRARY BOOK AVAILABILITY CHECKER =====")
print("Book Borrowed:", chosen_book)
print("Late Fee:", chosen_fee)
print("Updated Library Stock:", library)
print("=============================================")  