import random
import time
def slow_print3(text, delay=0.02):
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()
def slow_print(text, delay=0.05):
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()
def slow_print2(text, delay=0.03):
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()
def slow_print4(text, delay=0.02):
        for char in text:
            print(char, end="", flush=True)
            time.sleep(delay)
        print()
op=["5 push ups", "20 reverse curls", "10 leg raises", "50 squats", "50 jumping jacks", "Plank (at least 2 mins)", "5 burpees" "10 situps", "10 crunches", "strectching 1 min"]
chosen= random.choices(op)
ch2=random.choices(op)
slow_print("You punishment is...")
time.sleep(2)
slow_print2(f"{chosen} and {ch2}")
time.sleep(2)
slow_print3("So now what are you waiting for???")
time.sleep(0.5)
slow_print4("GOOOOO!!!!!!")