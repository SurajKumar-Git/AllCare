class Support_Plan:

    __support_plans = {}
    __id = 101
    __basic_plan = None

    @classmethod
    def add_support_plans(cls, plan_id, plan):
        cls.__support_plans.setdefault(plan_id, plan)
        cls.__id += 1
    
    @classmethod
    def get_plan(cls, plan_id):
        return cls.__support_plans.get(plan_id)
    
    @classmethod
    def get_all_plans(cls):
        return cls.__support_plans
    
    @classmethod
    def get_basic_plan(cls):
        return cls.__basic_plan
    
    @classmethod
    def set_basic_plan(cls):
        cls.__basic_plan = Support_Plan("Basic_plan", 5000, "Description")

    def __init__(self, plan_name, plan_price, plan_description):
        self.__plan_id = Support_Plan.__id
        self.__plan_name = plan_name
        self.__plan_price_per_month = plan_price
        self.__plan_description = plan_description
        Support_Plan.add_support_plans(self.__plan_id, self)
    
    def get_plan_id(self):
        return self.__plan_id
    
    def set_plan_name(self, new_plan_name):
        self.__plan_name = new_plan_name
    
    def get_plan_name(self):
        return self.__plan_name
    
    def set_plan_price(self, new_plan_price):
        self.__plan_price_per_month = new_plan_price
    
    def get_plan_price(self):
        return self.__plan_price_per_month
    
    def set_plan_description(self, new_description):
        self.__plan_description = new_description
    
    def get_plan_descripton(self):
        return self.__plan_description
    

    def __str__(self):
        return f"\nPlan Name:\t{self.get_plan_name()}\nPrice/month:\t{self.get_plan_price()}\nPlan Description:\t{self.get_plan_descripton()}\n"


Support_Plan.set_basic_plan()
Support_Plan("Champion Plan",7000,"Description")
Support_Plan("Best Plan",10000,"Description")