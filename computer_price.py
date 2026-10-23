class computer:
    def __init__(self,name):
        self.name=name
        self.__max_price= 3000
    def sell_price(self):
        print("Max price of the",self.name,"= $",self.__max_price)
    def change(self,price):
        self.__max_price=price
samsung_book=computer("samsung book")
samsung_book.sell_price()
samsung_book.change(5000)
samsung_book.sell_price()