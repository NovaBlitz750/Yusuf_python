class book:
    def __init__(self,title,author,is_borrowed):
        self.title=title
        self.autor=author
        self.is_borrowed=is_borrowed
    def borrow(self,title,is_borrowed):
        print(self.title,":borrowed")
        self.is_borrowed=True
    def return_book(self,title,is_borrowed):
        print(self.title,":borrowed")
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