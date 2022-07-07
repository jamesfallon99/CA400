import random
from unicodedata import category

from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
#User = get_user_model()
# Create your models here.
# class User(models.Model):
#     first_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100)
#     email_address = models.EmailField()
#     password = models.CharField(max_length=50)

#     def __str__(self):
#         return f"{self.first_name} {self.last_name} {self.email_address} {self.password}"
    
#     def get_first_name(self):
#         return self.first_name
    
#     def get_last_name(self):
#         return self.last_name
    
#     def get_email_address(self):
#         return self.email_address
    
#     def get_password(self):
#         return self.password

class Attraction(models.Model): #Places of interest stored in our database
    id = models.IntegerField(primary_key=True, unique=True)
    activity_title = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    averageRating = models.FloatField(null=True, blank=True) #Average review rating
    details = models.CharField(max_length=100, null=True, blank=True)

    def get_activity_title(self):
        return self.activity_title

    def get_address(self):
        return self.address

    def get_category(self):
        return self.category

    def get_latitude(self):
        return self.latitude

    def get_longitude(self):
        return self.longitude

    def get_average_rating(self):
        return self.averageRating

    def get_details(self):
        return self.details
    
    def get_id(self):
        return self.id

    @staticmethod
    def shuffle_attractions():
        attractions = list(Attraction.objects.all().filter(category='attraction'))  # starting value at 6 so when we minus by 5 we will stay in a positive range
        activity1 = random.choices(attractions)
        activity2 = random.choices(attractions)
        activity3 = random.choices(attractions)
        
        restaurant = list(Attraction.objects.all().filter(category='restaurant').filter(id__lte=29400)) # starting value at 6 so when we minus by 5 we will stay in a positive range
        restaurant1 = random.choices(restaurant)
        restaurant2 = random.choices(restaurant)
        restaurant3 = random.choices(restaurant)

        return activity1, activity2, activity3, restaurant1, restaurant2, restaurant3

# class Restaurant(models.Model):
#     activity_title = models.CharField(max_length=100)


class Review(models.Model):
    attraction = models.ForeignKey(Attraction, on_delete=models.CASCADE) #- when we set up events
    # user = models.ForeignKey(User, on_delete=models.CASCADE) #The foreign key in this case is a User object
    review = models.CharField(max_length=100)
    sentiment = models.IntegerField()

    def __str__(self):
        return f" Review: {self.review}, " \
               f" Sentiment: {self.sentiment}"

    def get_review(self):
        return self.review

    def get_user(self):
        return self.user

    def get_attraction(self):
        return self.attraction

    def get_sentiment(self):
        return self.sentiment



rate_choices = [
    (1, "1 - Never want to attend"),
    (2, "2 - Would not like to attend"),
    (3, "3 - Would attend"),
    (4, "4 - Would like to attend"),
    (5, "5 - Really want to attend")
]
class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    attraction = models.ForeignKey(Attraction, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=rate_choices) #Rating how liked or disliked an attraction is on a scale of 1-5

    def get_user(self):
        return self.user

    def get_attraction(self):
        return self.attraction

    def get_rating(self):
        return self.rating

    @staticmethod
    def split_rating_and_attraction_id(rating_and_id):
        rating_and_id = rating_and_id.split("+")
        rating_value = int(rating_and_id[0])
        attraction_id = int(rating_and_id[1])
        return rating_value, attraction_id
#null=True, blank=True
# class UserProfile(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     interests = models.ManyToManyField(Attraction)
#     rating = models.ForeignKey(Rating, on_delete=models.CASCADE)


ATTRACTION_CHOICES = [('park', 'park'), ('animal-attraction', 'animal-attraction'), ('monument', 'monument'), ('art-gallery', 'art-gallery'), ('botanic-garden', 'botanic-garden'), ('buildings-&-structures', 'buildings-&-structures'), ('theme-park', 'theme-park')]
#poi_list = ['bus stop', 'parking', 'train station', 'tourist office', 'information point', 'high street', 'shopping-district']
FOOD_TYPE_CHOICES = [('chinese', 'chinese'), ('thai', 'thai'), ('american', 'american'), ('burgers', 'burgers'), ('italian', 'italian'), ('chicken', 'chicken'), ('chipper', 'chipper'), ('fast-food', 'fast-food')]

class UserPreference(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, unique=True, primary_key=True)

    attraction_preference_1 = models.CharField(choices=ATTRACTION_CHOICES, max_length=100)
    attraction_preference_2 = models.CharField(choices=ATTRACTION_CHOICES, max_length=100)
    attraction_preference_3 = models.CharField(choices=ATTRACTION_CHOICES, max_length=100)

    food_preference_1 = models.CharField(choices=FOOD_TYPE_CHOICES, max_length=100)
    food_preference_2 = models.CharField(choices=FOOD_TYPE_CHOICES, max_length=100)
    food_preference_3 = models.CharField(choices=FOOD_TYPE_CHOICES, max_length=100)

    def get_user(self):
        return self.user

    def get_attraction_preference_1(self):
        return self.attraction_preference_1

    def get_attraction_preference_2(self):
        return self.attraction_preference_2

    def get_attraction_preference_3(self):
        return self.attraction_preference_3

    def get_food_preference_1(self):
        return self.food_preference_1

    def get_food_preference_2(self):
        return self.food_preference_2

    def get_food_preference_3(self):
        return self.food_preference_3


class Location(models.Model):
    location = models.CharField(max_length=100, null=True, blank=True)
    pathToModel = models.CharField(max_length=100)

    def get_path_to_model(self):
        return self.pathToModel

    def get_location(self):
        return self.location

    def __str__(self):
        return f"{self.location}"

LOCATION_CHOICES = [('London', "London")]
class Trip(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, unique=True, primary_key=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    arrivalDate = models.DateField()
    departureDate = models.DateField()

    def get_user(self):
        return self.user

    def get_location(self):
        return self.location

    def get_arrival_date(self):
        return self.arrivalDate

    def get_departure_date(self):
        return self.departureDate

class SimilarAttractions(models.Model):
    attraction = models.ForeignKey(Attraction, on_delete=models.CASCADE, unique=True, primary_key=True)
    similar_attraction1 = models.IntegerField(default=1)
    similar_attraction2 = models.IntegerField(default=1)
    similar_attraction3 = models.IntegerField(default=1)
    similar_attraction4 = models.IntegerField(default=1)
    similar_attraction5 = models.IntegerField(default=1)
    similar_attraction6 = models.IntegerField(default=1)
    similar_attraction7 = models.IntegerField(default=1)
    similar_attraction8 = models.IntegerField(default=1)
    similar_attraction9 = models.IntegerField(default=1)
    similar_attraction10 = models.IntegerField(default=1)
    similar_attraction11 = models.IntegerField(default=1)
    similar_attraction12 = models.IntegerField(default=1)
    similar_attraction13 = models.IntegerField(default=1)
    similar_attraction14 = models.IntegerField(default=1)
    similar_attraction15 = models.IntegerField(default=1)
    similar_attraction16 = models.IntegerField(default=1)
    similar_attraction17 = models.IntegerField(default=1)
    similar_attraction18 = models.IntegerField(default=1)
    similar_attraction19 = models.IntegerField(default=1)
    similar_attraction20 = models.IntegerField(default=1)
    similar_attraction21 = models.IntegerField(default=1)
    similar_attraction22 = models.IntegerField(default=1)
    similar_attraction23 = models.IntegerField(default=1)
    similar_attraction24 = models.IntegerField(default=1)
    similar_attraction25 = models.IntegerField(default=1)
    similar_attraction26 = models.IntegerField(default=1)
    similar_attraction27 = models.IntegerField(default=1)
    similar_attraction28 = models.IntegerField(default=1)
    similar_attraction29 = models.IntegerField(default=1)
    similar_attraction30 = models.IntegerField(default=1)
    similar_attraction31 = models.IntegerField(default=1)

    def get_similar_attraction1(self):
        return self.similar_attraction1

    def get_similar_attraction2(self):
        return self.similar_attraction2

    def get_similar_attraction3(self):
        return self.similar_attraction3

    def get_similar_attraction4(self):
        return self.similar_attraction4

    def get_similar_attraction5(self):
        return self.similar_attraction5

    def get_similar_attraction6(self):
        return self.similar_attraction6

    def get_similar_attraction7(self):
        return self.similar_attraction7

    def get_similar_attraction8(self):
        return self.similar_attraction8

    def get_similar_attraction9(self):
        return self.similar_attraction9

    def get_similar_attraction10(self):
        return self.similar_attraction10

class ActivityFeatures(models.Model):
    activity = models.ForeignKey(Attraction, on_delete=models.CASCADE, unique=True, primary_key=True)
    feature1 = models.CharField(max_length=100)
    feature2 = models.CharField(max_length=100)
    feature3 = models.CharField(max_length=100)
    feature4 = models.CharField(max_length=100)
    feature5 = models.CharField(max_length=100, null=True, blank=True)
    feature6 = models.CharField(max_length=100, null=True, blank=True)


    def get_feature1(self):
        return self.feature1

    def get_feature2(self):
        return self.feature2

    def get_feature3(self):
        return self.feature3

    def get_feature4(self):
        return self.feature4
    
    def get_feature5(self):
        return self.feature5
    
    def get_feature6(self):
        return self.feature6

class RestaurantFeatures(models.Model):
    restaurant = models.ForeignKey(Attraction, on_delete=models.CASCADE, unique=True, primary_key=True)
    feature1 = models.CharField(max_length=100)
    feature2 = models.CharField(max_length=100)
    feature3 = models.CharField(max_length=100)
    feature4 = models.CharField(max_length=100)
    feature5 = models.CharField(max_length=100, null=True, blank=True)
    feature6 = models.CharField(max_length=100, null=True, blank=True)

    def get_feature1(self):
        return self.feature1

    def get_feature2(self):
        return self.feature2

    def get_feature3(self):
        return self.feature3

    def get_feature4(self):
        return self.feature4

    def get_feature3(self):
        return self.feature5

    def get_feature4(self):
        return self.feature6
