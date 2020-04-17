class Rating_and_Review:

    __rating_and_reviews = [] #objects of rating and reviews


    @classmethod
    def get_all_ratings(cls):
        return  cls.__rating_and_reviews

    @classmethod
    def add_rating(cls, rating):
        cls.__rating_and_reviews.append(rating)
    
    def __init__(self, userid, username, rating, review):
        self.__userid = userid
        self.__username = username
        self.__rating = rating
        self.__review = review
        Rating_and_Review.add_rating(self)

    def get_userid(self):
        return self.__userid
    
    def get_username(self):
        return self.__username
    
    def get_rating(self):
        return self.__rating
    
    def get_review(self):
        return self.__review

    @classmethod
    def provide_rating(cls, userid, username):
        print("Give Rating to AllCare:")
        print("1. Bad\t2. Normal\t3. Average\t4. Good\t5.Very Good Service")
        while True:
            rating = input()
            if rating not in ("1","2","3","4","5"):
                print("Invalid Input. Please provide from 1 to 5")
            else:
                break
        print("Please provide your vaulable review on system:\n")
        review = input()
        Rating_and_Review(userid, username,int(rating),review)
        print("Thank you for your vaulable Inputs")
    
    @classmethod
    def view_all_ratings(cls):
        for rating in cls.get_all_ratings():
            print(rating)

    def __str__(self):
        return f"\nName:\t{self.get_username()}\nRating:\t{self.get_rating()}\nReview:\t{self.get_review()}\n"