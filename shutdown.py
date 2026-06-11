def shutdown():
    return "Shutting Computer"
    return False
apps=input("Are all of your apps closed?").strip().upper()
if apps=="Y" or apps=="YES":
    print(shutdown())
else:
    print("Close all of your apps then be ready for cumputer shutdown")