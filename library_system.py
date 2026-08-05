class book:
    def __init__(self,title,author,is_borrowed):
        self.title=title
        self.autor=author
        self.is_borrowed=is_borrowed
    def borrow(self,title,is_borrowed):
        print(self.title,": Borrowed")
        self.is_borrowed=True
    def return_book(self,title,is_borrowed):
        print(self.title,": In stock")
        self.is_borrowed=False
b1=book("Harry Potter","JK Rowling",False)
b2=book("Dexter Proctor","Adam Kay", False)
b3=book("Matilda","Roald Dahl",False)
print("Book availabilities:")
if b1.is_borrowed==True:
    b1.borrow("Harry Potter",True)
elif b1.is_borrowed==False:
    b1.return_book("Harry Potter",False)
if b2.is_borrowed==True:
    b2.borrow("Dexter Proctor",True)
elif b2.is_borrowed==False:
    b2.return_book("Dexter Proctor",False)
if b3.is_borrowed==True:
    b3.borrow("Matilda",True)
elif b3.is_borrowed==False:
    b3.return_book("Matilda",True)
while True:
    bor=input("Would you like to borrow or return a book?").strip().capitalize()
    if bor=="Borrow":
        whi=int(input("Which book would you like to borrow?: 1.Harry Potter 2.Dexter Proctor 3.Matilda "))
        if whi==1:
         b1.borrow("Harry Potter",True)
        elif whi==2:
         b2.borrow("Dexter Proctor",True)
        else:
         b3.borrow("Matilda",True)
    elif bor=="Return":
        wh=input("Which book would you like to return?: 1.Harry Potter 2.Dexter Proctor 3.Matilda ")
        if wh==1:
            b1.return_book("Harry Potter",False)
        elif wh==2:
            b2.return_book("Dexter Proctor",False)
        else:
            b3.return_book("Matilda",False)
    else:
            print("Please enter a valid input")
