from .Users import User
from .Support_Plan import Support_Plan

class Elder(User):

    __elders = {}
    
    @classmethod
    def add_elder(cls, user_id, elder):
        cls.__elders.setdefault(user_id, elder)

    @classmethod
    def get_elder(cls, user_id):
            return cls.__elders.get(user_id)

    @classmethod
    def get_elders_list(cls):
        return cls.__elders
    
    @classmethod
    def check_user(cls, userid):
        return userid in cls.__elders


    def __init__(self, name, password, dob, phone_number, address):

        super().__init__(name, password, dob, phone_number, address)
        self.__available_status = True
        self.__requests = {} #userid: username
        self.__care_provider = None #userid
        self.__care_plan = None # (plan ID, plan Name)
        Elder.add_elder(self.get_userid(), self)
        
    
    def switch_available_status(self):
        self.__available_status = False if self.get_status() else True
    
    def view_available_status(self):
        return "Available" if self.get_status() else "Not Available"


    def get_status(self):
        return self.__available_status

    def set_care_provider(self, user_id):
        self.__care_provider = user_id

    def get_care_provider(self):
        return self.__care_provider
    
    def set_care_plan(self, plan_id, plan_name):
        self.__care_plan = (plan_id, plan_name)
    
    def get_care_plan(self):
        return self.__care_plan

    def get_requests(self):
        return self.__requests
    
    def clear_requests(self, *args):
        if args:
            if self.get_requests().pop(args[0], None):
                CareProvider.get_care_provider(args[0]).clear_request_made(self.get_userid())
        else:
            for userid in self.get_requests().copy():
                CareProvider.get_care_provider(userid).clear_request_made(self.get_userid())
            self.get_requests().clear()

    def add_requests(self, careprovider_id):
        self.__requests.setdefault(careprovider_id, CareProvider.get_care_provider(careprovider_id).get_name())

    def view_requests(self):
        while True:
            if not self.get_care_provider():
                if self.get_requests():
                    for userid, name in self.get_requests().items():
                        print(f"{userid}\t{name}")
                    print("\nEnter User ID to ViewCareTaker Information/Approve/Reject request\n-1 to exit")
                    user_id = int(input())
                    if user_id == -1:
                        return
                    if user_id in self.get_requests():
                        while True:
                            print("1. View\t2. Approve\t3. Reject\t-1 to Return")
                            option = int(input())
                            if option == 1:
                                print(CareProvider.get_care_provider(user_id))
                            elif option == 2:
                                self.approve_request(user_id)
                                print("Request has been approved")
                                return
                            elif option == 3:
                                self.reject_request(user_id)
                                print("Request has been rejected")
                                break
                            else:
                                break
                    else:
                        print("Invalid UserID. Please enter Valid User ID")
                else:
                    print("No requests found")
                    break
            else:
                print("You are already have caretaker:",self.get_care_provider())
                break

    def approve_request(self, user_id):
        careprovider = CareProvider.get_care_provider(user_id)
        self.set_care_provider(user_id)
        basicplan = Support_Plan.get_basic_plan()
        self.set_care_plan(basicplan.get_plan_id(), basicplan.get_plan_name())
        careprovider.add_care_member(self.get_userid())
        self.clear_requests()
    
    def reject_request(self, user_id):
        self.clear_requests(user_id,)
    
    def view_careprovider_details(self):
        if self.get_care_provider():
            print(CareProvider.get_care_provider(self.get_care_provider()))
        else:
            print("No Careprovider assigned")
    
    def view_my_support_plan(self):
        if self.get_care_provider():
            planid, plan_name = self.get_care_plan()
            print(f"\nPlan ID:\t{planid}\nPlan_Name:\t{plan_name}\n")
            print("Enter 1 to make changes to Support Plan or other key to return")
            if input() == "1":
                self.view_support_plans()
                print("Enter Plan ID to make changes or -1 to return")
                while True:
                    planid = int(input())
                    if planid != -1:
                        if self.change_care_plan(planid):
                            print("Plan successfully changed")
                            return
                        else:
                            print("Invalid Plan ID, Please Enter valid planID or -1 to return")
                    else:
                        return
            else:
                return
        else:
            print("You do not have any care provider assigned to you")
    
    def change_care_plan(self, plan_id):
        plan = Support_Plan.get_plan(plan_id)
        if plan:
            self.set_care_plan(plan_id, plan.get_plan_name())
            CareProvider.get_care_provider(self.get_care_provider()).change_care_members_plan(self.get_userid(), plan_id, plan.get_plan_name())
            return 1
        else:
            return 0


#-------------------CareProvider class---------------------
class CareProvider(User):
    __careproviders = {}
    __elders_care_limit = 4

    @classmethod
    def add_care_provider(cls, id, careprovider):
        cls.__careproviders.setdefault(id, careprovider)

    @classmethod
    def get_care_provider(cls, userid):
        return cls.__careproviders.get(userid)

    @classmethod
    def get_care_providers_list(cls):
        return cls.__careproviders

    @classmethod
    def get_care_limit(cls):
        return cls.__elders_care_limit
    
    @classmethod
    def check_user(cls, userid):
        return userid in cls.__careproviders


    def __init__(self, name, password, dob, phone_number, address):
        super().__init__(name, password, dob, phone_number, address)
        self.__elder_care_members = {} #userid: username
        self.__count = 0    
        # self.__rating_and_reviews = []
        self.__requests_made = {} #userid: username
        self.__care_members_plans = {} #userid : [planid, plan_name]
        CareProvider.add_care_provider(self.get_userid(), self)

    def add_requests_made(self, user_id, name):
        self.__requests_made.setdefault(user_id, name)
    
    def get_requests_made(self):
        return self.__requests_made

    def get_care_members(self):
        return self.__elder_care_members
    
    def add_care_member(self, user_id):
        self.__elder_care_members.setdefault(user_id, Elder.get_elder(user_id).get_name())
        self.assign_basic_plan(user_id)
        self.update_count()
        if self.get_count() == CareProvider.get_care_limit(): # Clear all request of the user when care limit is reached.
            self.clear_request_made()

    def get_count(self):
        return self.__count

    def update_count(self):
        self.__count = len(self.get_care_members())
    
    def assign_basic_plan(self,user_id):
        basic_plan = Support_Plan.get_basic_plan()
        self.set_care_members_plan(user_id, basic_plan.get_plan_id(), basic_plan.get_plan_name())
    
    def change_care_members_plan(self, user_id, plan_id, plan_name):
        self.set_care_members_plan(user_id , plan_id, plan_name)
    
    
    def set_care_members_plan(self, user_id, plan_id, plan_name):
        self.__care_members_plans[user_id] =  [plan_id, plan_name]
        
    def get_care_members_plan(self):
        return self.__care_members_plans

    def view_mycare_members(self):
        if self.get_care_members():
            print("UserID\tName")
            for user_id, name in self.get_care_members().items():
                print(f"{user_id}\t{name}")
        else:
            print("You do not have any care member assigned.")
        
    def view_elders_list(self):
        print("UserID \t Name")
        for userid, elder in Elder.get_elders_list().items():
            if elder.get_status() and not elder.get_care_provider():
                print(f"{userid}\t{elder.get_name()}")
        if self.get_count() < CareProvider.get_care_limit():
            while True:
                print("Enter User ID Make request for care/View Elder Infomation or -1 to exit:")
                userid = int(input())
                if userid != -1:
                    if Elder.check_user(userid):
                        while True:
                            print("Enter \t1. View Information \t2. Make request for care\t-1 to return")
                            option = int(input())
                            if option == 1:
                                print(Elder.get_elder(userid))
                            elif option == 2:
                                if self.make_request(userid):
                                    print("Request has been made awaiting approval")
                                    break
                                else:
                                    print(f"Request for this userid: {userid} is already made.")
                                    
                            else:
                                break
                    else:    
                        print("Invalid UserID, Please Enter valid User ID")
                else:
                    return
        else:
            print(f"You cannot make more requests. Since you already have {CareProvider.get_care_limit()} members under your care")

    def make_request(self, userid):
        if userid not in self.get_requests_made():
            elder = Elder.get_elder(userid)
            elder.add_requests(self.get_userid())
            self.add_requests_made(elder.get_userid(), elder.get_name())
            return 1
        else:
            return 0


    def clear_request_made(self, *args):
        if args:
            if self.get_requests_made().pop(args[0], None):
                Elder.get_elder(args[0]).clear_requests(self.get_userid())
        else:
            for userid in self.get_requests_made().copy():
                Elder.get_elder(userid).clear_requests(self.get_userid())
            self.get_requests_made().clear()
                    

    def view_request_made(self):
        while True:
            if self.get_requests_made():
                for userid, name in self.get_requests_made().items():
                    print(f"{userid}\t{name}")
                print("Enter userid to cancel request or 0 to cancel all requests or -1 to exit")
                userid = int(input())
                if userid == -1:
                    return
                elif userid == 0:
                    self.clear_request_made()
                    print("All Request have been cleared")
                    return
                elif userid in self.get_requests_made():
                    self.clear_request_made(userid)
                    print(f"UserId: {userid} \nRequest has been cancel")
                else:
                    print("InValid user id/option, Please Enter valid userid/option")
            else:
                print("No requests found")
                return

    def view_mycare_members_plans(self):
        if self.get_care_members():
            print("Name\tPlan ID\tPlan Name")
            for userid, (planid, plan_name) in self.get_care_members_plan().items():
                user = Elder.get_elder(userid)
                print(f"{user.get_name()}\t{planid}\t{plan_name}")
        else:
            print("Enter You do not have any care members")
