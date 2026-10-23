class DailyMessage:
    def __init__(self):
        self.message = ""

    def get_user_input(self):
        self.message = input("Enter today's message: ").strip()

    def display_upper(self):
        if self.message:
            print(f"Today's message is: {self.message.upper()}")
        else:
            print("No message was entered.")


class HelperSession:
    def __init__(self):
        print("[INFO] Session initialized successfully.")

    def __del__(self):
        print("[INFO] Session destroyed successfully.")

    @classmethod
    def start_session(cls):
        print("Launching a new helper session...")
        return cls()


class PairFinder:
    def __init__(self, numbers):
        self.numbers = numbers

    def find_target_pair(self, target):
        seen = {}
        for index, num in enumerate(self.numbers):
            complement = target - num
            if complement in seen:
                return seen[complement], index
            seen[num] = index
        return None


def main():
    messenger = DailyMessage()
    messenger.get_user_input()
    messenger.display_upper()
    print("-" * 30)

    print("Creating session...")
    session_obj = HelperSession.start_session()
    print("-" * 30)

    dataset = (10, 20, 30, 40, 50, 60, 70)
    
    try:
        target_value = int(input("Enter target sum to search: "))
    except ValueError:
        print("Invalid input. Please enter a whole number.")
        return

    finder = PairFinder(dataset)
    result = finder.find_target_pair(target_value)

    if result:
        print(f"Match found! Index 1: {result[0]}, Index 2: {result[1]}")
    else:
        print("No matching pair found for that target.")
    print("-" * 30)

    print("Cleaning up resources...")
    del session_obj
    print("Program finished.")


if __name__ == "__main__":
    main()
