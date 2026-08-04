"Question 1: Bankacc"
class bankac:
    __balance=500
    def pri_balance(self):
        print("Ur bank account has $",self.__balance)
customer=bankac()
customer.pri_balance()
"Question 2: Student"
class stu:
    __marks=90
    def pri_marks(self):
        print("The student has obtained", self.__marks, "marks")
kid=stu()
kid.pri_marks()
class game:
    __score=100
    def pri_score(self):
        print("The score is",self.__score)
gamee=game()
gamee.pri_score()