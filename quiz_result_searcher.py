quiz_scores=[32,75,90,38,62,40,84,45,23,13,43,54]
print("QUIZ RESULT SEARCHER")
print("All quiz scores:",quiz_scores)
first_score = quiz_scores[0]
print("Time Complexity: O(1)")
print("Theta Notation: Theta(1)")
print("Reason being; direct access takes only 1 step")
target=int(input("Enter a score result to find "))
steps=0
for i,score in enumerate(quiz_scores):
    steps+=1
    if score==target:
        print(target,"found at",i,"position")
        break
    else:
        pass
print("Time complexity: O(i)")
print("Reason: score is found on i number of times")
step1=0
for i in quiz_scores:
    for i in quiz_scores:
        step1+=1
print("Time complexity: O(i^2)")
print("Reason: i is ran in 2 loops")