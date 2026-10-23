import time
seconds=int(input(("Enter the amount of seconds")))
for i in range(seconds, 0, -1):
    print(i)
    time.sleep(1)
print("Times up!")