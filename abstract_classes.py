from abc import ABC, abstractmethod
class abstract_class(ABC):
    def print_val(self):
        print("This is abstract class")
    @abstractmethod
    def task(self):
        print("Inside an abstract method")
class test_class(abstract_class):
    def task(self):
        print("This is child class")
to=test_class()
to.print_val()
to.task()