"""
School Snack Counter
Sets and Arrays

This program builds a "School Snack Counter" that:
1. Creates snack boxes using sets
2. Adds new snacks to a set
3. Finds shared snacks between two boxes
4. Creates an array (list) of snack counts
5. Adds values to that array
6. Uses count() and reverse() to explore the final result
"""

# 1. Create snack boxes with sets
box_a = {"chips", "pretzels", "apple", "granola bar"}
box_b = {"apple", "crackers", "granola bar", "juice box"}

print("Box A snacks:", box_a)
print("Box B snacks:", box_b)

# 2. Add a new snack to a set
box_a.add("cookies")
print("\nAfter adding a new snack to Box A:")
print("Box A snacks:", box_a)

# 3. Find shared snacks between the two boxes
shared_snacks = box_a.intersection(box_b)
print("\nSnacks shared between Box A and Box B:", shared_snacks)

# 4. Create an array (list) of snack counts
# Each number represents how many of that snack were counted that day
snack_counts = [3, 5, 2, 8, 4]
print("\nInitial snack counts array:", snack_counts)

# 5. Add values to the array
snack_counts.append(6)      # add a new count to the end
snack_counts.insert(0, 10)  # add a count to the beginning
print("Snack counts after adding new values:", snack_counts)

# 6. Use count() and reverse() to explore the final result
how_many_fours = snack_counts.count(4)
print(f"\nThe number 4 appears {how_many_fours} time(s) in the snack counts array.")

snack_counts.reverse()
print("Snack counts array reversed:", snack_counts)

# Final summary
print("\n--- Final Summary ---")
print("Shared snacks:", shared_snacks)
print("Final snack counts (reversed):", snack_counts)