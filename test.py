from AllCareApp.Elders_and_CareProvider import Elder, CareProvider
from datetime import date
from IPython.display import clear_output
from AllCareApp.Users import User

class Test:

    @classmethod
    def start(cls):
        print("Enter 1. Login 2. Register OtherKey to Exit")
        option = input()
        if option == "1":
            cls.login()
        elif option == "2":
            cls.register()
        else:
            return

    @classmethod
    def login(cls):
        print("Enter User ID and Password or -1 to exit")
        attempt = 1
        while True:
            userid = int(input())
            if userid != -1:
                password = input()
                user = User.get_user(userid)
                if user:
                    if user[0] == password:
                        cls.showinterface(userid, user[1])
                        return
                
                print("Invalid userid or password. Please Enter Correct User id and password or -1 to exit.")
                attempt += 1
                if attempt == 3:
                    return
        
    @classmethod
    def register(cls):
        print("No yet implemented.")
    
    @classmethod
    def showinterface(cls, userid, usertype):
        if usertype == Elder:
            user = Elder.get_elder(userid)
            cls.show_elder_interface(user)
        else:
            user = CareProvider.get_care_provider(userid)
            cls.show_care_provider_interface(user)
    
    @classmethod
    def show_elder_interface(cls, user):
        while True:
            clear_output(wait=True)
            print(f"\nHi, {user.get_name()}\t\t\tYou are {user.view_available_status()} for care")
            print("\nEnter\n1. Switch Available Status\n2. View Requests for care\n3. View All Care Plans\n4. View My Care Plan\n5. View my caretaker details\n6. Give rating and review to All Care\n7. View rating and review to All Care\nOther Key to Log Out")
            option = input()
            if option == "1":
                user.switch_available_status()
            elif option == "2":
                user.view_requests()
            elif option == "3":
                user.view_support_plans()
            elif option == "4":
                user.view_my_support_plan()
            elif option == "5":
                user.view_careprovider_details()
            elif option == "6":
                user.give_ratings()
            elif option == "7":
                user.view_ratings()
            else:
                print("Logout")
                return
            print("press any key to continue")
            input()
    
    @classmethod
    def show_care_provider_interface(cls, user):
        while True:
            clear_output(wait=True)
            print(f"\nHi, {user.get_name()}")
            print("\nEnter\n1. View Elders list to make request\n2. View sent requests\n3. View MyCare Members\n4. View All Care Plans\n5. View My Care Plan\n6. Give rating and review to All Care\n7. View rating and review to All Care\nOther Key to Log Out")
            option = input()
            if option == "1":
                user.view_elders_list()
            elif option == "2":
                user.view_request_made()
            elif option == "3":
                user.view_mycare_members()
            elif option == "4":
                user.view_support_plans()
            elif option == "5":
                user.view_mycare_members_plans()
            elif option == "6":
                user.give_ratings()
            elif option == "7":
                user.view_ratings()
            else:
                print("Logout")
                return
            print("press any key to continue")
            input()