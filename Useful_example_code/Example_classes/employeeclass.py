
import datetime


class Employee:
    # class variable:
    num_of_employees = 0
    raise_amount = 1.04

    # initialisations
    def __init__(self, first_name: str, last_name: str, pay: int):
        self.first_name = first_name
        self.last_name = last_name
        self.pay = pay
        #self.email = ((f'{first_name}.{last_name}@company.com')).lower()
        #self.fullname = (f'{first_name} {last_name}')

        Employee.num_of_employees += 1
    '''
        property decorator allows you to use a method as a property 
    '''
    #__________________________________________________________
    @property
    def email(self):
        return(f'{self.first_name}.{self.last_name}@email.com')
    @property
    def fullname(self):
        return(f'{self.first_name} {self.last_name}')

    #_________________________________________
    @fullname.setter
    def fullname(self,name):
        first_name,last_name = name.split(' ')
        self.first_name = first_name
        self.last_name = last_name

    @fullname.deleter
    def fullname(self):
        print('Deleted Name')
        self.first_name=None
        self.last_name=None

    # ______________________________________________________________
    def apply_raise(self):

        self.pay = int(self.pay * self.raise_amount)
        pass
    # ____________________________________________________________________

    @classmethod  # class Method decorater
    def set_raise_amt(cls, amount):
        cls.raise_amount = amount
        # this method is the same as doing Employee.raise_amount = amount
        # set changes to class variables which will apply to the entire class, unless over-written by instance daclaration or subclass variables
        pass

    # _________________________________________________________________
    @classmethod
    def from_string(cls, emp_string):
        first_name, last_name, pay = emp_string.split('-')
        return cls(first_name, last_name, pay)

    # _______________________________________________________________________________________________________________
    # static methods have a logical connection to the class, but do not recieve
    @staticmethod
    def is_workday(day):        # any class varibles or instance variables
        if day.weekday() == 5 or day.weekday() == 6:
            return False
        return True

    # _______________________________________________________________________________________
    def __repr__(self):  # used to make the object unambiguous
        return (f'Fist Name: {self.first_name},Last Name: {self.last_name},Pay: {self.pay}')

    def __str__(self):  # used to make a readable representation
        return (f'{self.fullname} - {self.email}')


'''
Inheritance:
'''


class Developer(Employee):

    raise_amount = 1.10

    def __init__(self, first_name: str, last_name: str, pay: int, prog_lang: str):
        super().__init__(first_name, last_name, pay)
        # Employee.__init__(self,first_name,last_name,pay) >> also calls the parent class, useful when the file has multiple inheritences
        self.prog_lang = prog_lang


class Manager(Employee):

    def __init__(self, first_name: str, last_name: str, pay: int, employees: list = None):
        super().__init__(first_name, last_name, pay)
        if employees is None:
            self.employees = []
        else:
            self.employees = employees

    def add_employee(self, employee):
        if employee not in self.employees:
            self.employees.append(employee)

    def remove_employee(self, employee):
        if employee in self.employees:
            self.employees.remove(employee)

    def print_employees(self):
        for count, emp in enumerate(self.employees, 1):
            print(count, emp.fullname)


# ___________________________________________________________
my_date = datetime.date(2021, 5, 3)
# print(Employee.is_workday(my_date)) # return true of my_date is a work day (Mon - Friday)
# _____________________________________________________________


emp1 = Employee('Kelvin', 'User', 50000)
emp2 = Employee('Sam', 'User', 60000)

# ____________________________________________________________
emp_string = 'John-Doe-70000'
# uses the class method from_string to create a new employee
new_emp = Employee.from_string(emp_string)

# _______________________
# assigns a priority instance variable specific to the emp1 instance called raise_amount
emp1.raise_amount = 1.05
# assigns a secondary attribut to all instances but does not overide instance defined attribute of the same name
Employee.raise_amount = 1.06
Employee.set_raise_amt(1.06)  # does the same thing as above

'''
Inheritance 
'''
# Developer Instance
'''
dev_1 = Developer('Boris', 'Johnson', 110000, 'C#')
dev_2 = Developer('Wayne', 'Rooney', 540000, 'Java')
# print(help(Developer)) # returns all information about this sub class including all of its inherited properties
print(dev_1.fullname)
print(dev_2.email)
print(dev_2.prog_lang)
'''

#instance for manager
'''
manager_1 = Manager('Sue', 'Morris', 780000, [dev_1, dev_2])
print(manager_1.email)
manager_1.print_employees()
'''

# __repr__ & __str__
'''
print(emp1.__repr__())
print(emp1.__str__())# if __str__() not available, this fall back to call __repr__
print(emp1)  # same as above, defaults to __str__() if available else, resets to __repr__
'''

print(emp1.email)
emp1.fullname = 'Cliff Chavhu'
print(emp1.email)
del emp1.fullname
print(emp1.first_name)
print(emp2.fullname)
#print(emp1.__dict__) # print all the attributes attached to the instance
print(Employee.num_of_employees)
print(new_emp.fullname)
