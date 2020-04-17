from .Support_Plan import Support_Plan
from .Rating_and_Review import Rating_and_Review


class User:
    id = 1000

    __users = {}  # userid: [password, usertype]
    @classmethod
    def generateID(cls):
        cls.id += 1
        return cls.id


    @classmethod
    def calculateAge(cls, dob):
        import datetime
        today = datetime.date.today()
        return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

    @classmethod
    def adduser(cls, userid, password, usertype):
        cls.__users.setdefault(userid, [password, usertype])

    @classmethod
    def get_user(cls, userid):
        return cls.__users.get(userid)

    def __init__(self, name, password, dob, phone_number, address):
        self.__userid = User.generateID()
        self.__name = name
        self.__password = password
        self.__dob = dob
        self.__age = User.calculateAge(dob)
        self.__phone_number = phone_number
        self.__address = address
        User.adduser(self.__userid, password, type(self))

    def set_address(self, new_address):
        self.__address = new_address

    def get_userid(self):
        return self.__userid

    def set_password(self, newpassword):
        self.__password = newpassword

    def get_password(self):
        return self.__password

    def get_name(self):
        return self.__name

    def get_dob(self):
        return self.__dob

    def get_age(self):
        return self.__age

    def get_address(self):
        return self.__address

    def set_phone_number(self, new_phone_number):
        self.__phone_number = new_phone_number

    def get_phone_number(self):
        return self.__phone_number

    # ---------------Common Functionanlities----

    def give_ratings(self):
        Rating_and_Review.provide_rating(self.get_userid(), self.get_name())

    def view_ratings(self):
        Rating_and_Review.view_all_ratings()

    def view_support_plans(self):
        for plan_id, plan in Support_Plan.get_all_plans().items():
            print(f"\nPlan_ID:\t{plan_id}{plan}")

    def __str__(self):
        return f"User Information\nName:\t{self.get_name()}\nAge:\t{self.get_age()}\nDOB:\t{self.get_dob()}\nPhoneNumber:\t{self.get_phone_number()}\nAddress:\t{self.get_address()}\n"
