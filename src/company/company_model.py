import abc


class Company(object):
    """Represents a company"""

    def __init__(self, name, address=None):
        self.name = name
        self.address = address
        self.employees = list()
        self.__money = 1000

    def add_employee(self, employee):
        if not employee.is_employed and (
            isinstance(employee, Engineer) or isinstance(employee, Manager)
        ):
            self.employees.append(employee)
            employee.join_company(self)

    def dismiss_employee(self, employee):
        """
        Dismisses an employee. Employee must be a company member.
        Company should notify employee that he/she was dismissed
        """
        if employee in self.employees:
            self.employees.remove(employee)
            employee.notify_dismissed()

    def notify_im_leaving(self, employee):
        """En employee should call this method when leaving a company"""
        self.employees.remove(employee)

    def do_tasks(self, employee):
        """
        Engineer should call this method when he is working.
        Company should withdraw 10 money from a personal account and return
        them to engineer. That will be a payment
        :rtype: int
        """
        if employee in self.employees and isinstance(employee, Engineer):
            self.__money -= 10
            return 10
        else:
            raise Exception(f"{employee} is not work in {self.name}")

    def write_reports(self, employee):
        """
        Manager should call this method when he is working.
        Company should withdraw 12 money from a personal account and return
        them to manager. That will be a payment
        :rtype: int
        """
        if employee in self.employees and isinstance(employee, Manager):
            self.__money -= 12
        return 12

    def make_a_party(self):
        """Party time! All employees get 5 money"""
        if not self.is_bankrupt and self.__money - len(self.employees) * 5 > 0:
            for employee in self.employees:
                employee.bonus_to_salary(self)

    def show_money(self):
        """Displays amount of money that company has"""
        return "%s balance is: %s dollars" % (self.name, self.__money)

    def go_bankrupt(self):
        """
        Declare bankruptcy. Company money are drop to 0.
        All employees become unemployed.
        """
        self.__money = 0
        for employee in self.employees:
            employee.become_unemployed()

    @property
    def is_bankrupt(self):
        """returns True or False"""
        return self.__money <= 0

    def __repr__(self):
        return "Company (%s)" % self.name


class Person(object):
    """Represents any person"""

    def __init__(self, name, age, sex=None, address=None):
        self.name = name
        self.age = age
        self.sex = sex if sex is not None else "<not specified>"
        self.address = address

    def __repr__(self):
        return "%s, %s years old" % (self.name, self.age)


class Employee(Person, metaclass=abc.ABCMeta):
    def __init__(self, name, age, sex=None, address=None):
        super().__init__(name, age, sex, address)
        self.company = None
        self.__money = 0

    def join_company(self, company):
        if not self.is_employed:
            self.company = company
            company.employees.append(self)
        else:
            raise AttributeError(f"{self.name} is already employed")

    def become_unemployed(self):
        """Leave current company"""
        self.company.notify_im_leaving(self)
        if self.is_employed:
            self.company = None

    def notify_dismissed(self):
        """Company should call this method when dismissing an employee"""
        if self.is_employed or self.company.is_bankrupt:
            self.company = None

    def bonus_to_salary(self, company, reward=5):
        """
        Company should call this method on each employee when having a party
        """
        if self in company.employees:
            self.put_money_into_my_wallet(reward)

    @property
    def is_employed(self):
        """returns True or False"""
        return self.company is not None

    def put_money_into_my_wallet(self, amount):
        """Adds the indicated amount of money to persons budget"""
        raise NotImplementedError()

    def show_money(self):
        """Shows how much money person has earned"""
        raise NotImplementedError()

    @abc.abstractmethod
    def do_work(self):
        """This method requires re-implementation"""
        raise NotImplementedError()

    def __repr__(self):
        if self.is_employed:
            return "%s works" % (self.name)
        return "I am %s, my age is %s" % (self.name, self.age)


class Engineer(Employee):
    def __init__(self, name, age, sex=None, address=None):
        super(Employee, self).__init__(name, age, sex, address)
        self.company = None
        self._money = 0

    def do_work(self):
        if self.is_employed:
            amount = self.company.do_tasks(self)
            self.put_money_into_my_wallet(amount)
        else:
            raise AttributeError(f"{self.name} is not employed to have a work")

    def put_money_into_my_wallet(self, amount):
        """Adds the indicated amount of money to persons budget"""
        self._money += amount

    def show_money(self):
        """Shows how much money person has earned"""
        print("%s has %s dollars" % (self.name, self._money))


class Manager(Employee):
    def __init__(self, name, age, sex=None, address=None):
        super(Employee, self).__init__(name, age, sex, address)
        self.company = None
        self.__money = 0

    def do_work(self):
        amount = self.company.write_reports(self)
        self.put_money_into_my_wallet(amount)

    def put_money_into_my_wallet(self, amount):
        """Adds the indicated amount of money to persons budget"""
        self.__money += amount

    def show_money(self):
        """Shows how much money person has earned"""
        print("%s has %s dollars" % (self.name, self.__money))


class AlexSingleton(Engineer):
    __instance = None

    def __init__(self, name, age, sex=None, address=None):
        super().__init__(name, age, sex, address)
        if self.__instance is not None:
            raise RuntimeError("AlexSingleton class is already instantiated")
        AlexSingleton.__instance = self
        AlexSingleton.__instance.name = self.name
        AlexSingleton.__instance.age = self.age

    @classmethod
    def instance(cls):
        return cls.__instance
