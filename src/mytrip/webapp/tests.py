# from atexit import register
# from http import HTTPStatus
# from urllib import request, response
from django.test import TestCase, Client
from django.urls import reverse, resolve

from .models import Attraction, Review, Rating, UserPreference, Location, Trip
from .views import registerPage, sign_in, home, user_interests, create_trip, view_event, logoutUser
from django.contrib.auth.models import User
from datetime import date
# import json

# Create your tests here.
class TestUrls(TestCase):
#Testing all our endpoints
    def test_register_url(self):
        url = reverse('register') #get the url for register
        self.assertEquals(resolve(url).func, registerPage)
        #assert the register url function is registerPage

    def test_sign_in_url(self):
        url = reverse('sign-in')
        self.assertEquals(resolve(url).func, sign_in)

    def test_home_url(self):
        url = reverse('home')
        self.assertEquals(resolve(url).func, home)

    def test_user_interests_url(self):
        url = reverse('user-interests')
        self.assertEquals(resolve(url).func, user_interests)

    def test_create_trip_url(self):
        url = reverse('create-trip')
        self.assertEquals(resolve(url).func, create_trip)

    def test_logout(self):
        url = reverse('logout')
        self.assertEquals(resolve(url).func, logoutUser)

class TestViews(TestCase):


    def setUpTests(self):
        self.client = Client()

    def create_user(self):
        user = User.objects.create_user(username="test1", email="test@gmail.com", password="test2022")
        user.save()
        return user

    def test_register_GET_request(self):

        response = self.client.get(reverse('register')) #GET the register page

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'webapp/register.html') #Assert the register html page was used. Check if it is contained in the response

    def test_sign_in_GET_request(self):

        response = self.client.get(reverse('sign-in'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'webapp/sign-in.html')

    #In order to test the home page, we will need to log in a user
    def test_sign_in_and_access_home_page(self):
        #self.client.post()
        TestUser().create_user()
        self.client.login(username="test1", password="test2022")
        response = self.client.get(reverse("home"))
        self.assertTemplateUsed(response, 'webapp/index.html')


    def test_sign_in_post_request(self):
        self.create_user()
        response = self.client.post("/sign-in", data={'username': 'test1', 'password': 'test2022'})
        self.assertEqual(response.status_code, 302) #username and password were excepted as reponse code 302 indicates a redirect occurred.

    def test_registration_post_request(self):
        response = self.client.post(reverse('register'), {'username': 'test1', 'email': 'test@gmail.com', 'password1': 'test2022', 'password2': 'test2022'})
        self.assertEquals(response.status_code, 302)


    def test_user_interests_get_request(self): #At the moment the test case doesn't have any attractions in the test database. Therefore we get an error when we try to test this get request
        #Need to create attractions
        attraction_model = TestAttractionModel()
        attraction_model.create_attraction_objects()
        test_user = TestUser()
        test_user.create_user()
        self.client.login(username="test1", password="test2022")
        response = self.client.get(reverse('user-interests'))
        self.assertEquals(response.status_code, 200)


    # Test registering user with username already taken
    # Test invalid registration details

class TestAttractionModel(TestCase):
    def create_attraction_objects(self):
        #attraction1 = Attraction(activity_title, address, category, latitude, longitude, averageRating, details)
        attraction1 = Attraction(1, "The pub", "London City", "restaurant", 1234554.0093, 123454325.653, 60.0, "details")
        attraction1.save()
        attraction2 = Attraction(2, "The pub", "London City", "restaurant", 1234554.0093, 123454325.653, 60.0, "details")
        attraction2.save()
        attraction3 = Attraction(3, "The pub", "London City", "restaurant", 1234554.0093, 123454325.653, 60.0, "details")
        attraction3.save()
        attraction4 = Attraction(4, "The pub", "London City", "restaurant", 1234554.0093, 123454325.653, 60.0, "details")
        attraction4.save()
        attraction6 = Attraction(5, "The pub", "London City", "restaurant", 1234554.0093, 123454325.653, 60.0, "details")
        attraction6.save()
        attraction7 = Attraction(6, "The pub", "London City", "restaurant", 1234554.0093, 123454325.653, 60.0, "details")
        attraction7.save()
        attraction8 = Attraction(7, "The pub", "London City", "restaurant", 1234554.0093, 123454325.653, 60.0, "details")
        attraction8.save()
        attraction9 = Attraction(8, "The pub", "London City", "restaurant", 1234554.0093, 123454325.653, 60.0, "details")
        attraction9.save()
        attraction10 = Attraction(9, "The pub", "London City", "restaurant", 1234554.0093, 123454325.653, 60.0, "details")
        attraction10.save()
        attraction11 = Attraction(10, "The pub", "London City", "restaurant", 1234554.0093, 123454325.653, 60.0, "details")
        attraction11.save()
        attraction12 = Attraction(11, "The pub", "London City", "restaurant", 1234554.0093, 123454325.653, 60.0, "details")
        attraction12.save()
        attraction13 = Attraction(12, "The pub", "London City", "restaurant", 1234554.0093, 123454325.653, 60.0, "details")
        attraction13.save()
        attraction14 = Attraction(13, "The pub", "London City", "restaurant", 1234554.0093, 123454325.653, 60.0, "details")
        attraction14.save()
        attraction15 = Attraction(14, "The pub", "London City", "restaurant", 1234554.0093, 123454325.653, 60.0, "details")
        attraction15.save()
        attraction16 = Attraction(15, "The pub", "London City", "restaurant", 1234554.0093, 123454325.653, 60.0, "details")
        attraction16.save()

    def test_attraction(self):
        self.create_attraction_objects()
        attraction = Attraction.objects.get(pk=1)
        activity_title = attraction.get_activity_title()
        address = attraction.get_address()
        category = attraction.get_category()
        latitude = attraction.get_latitude()
        longitude = attraction.get_longitude()
        details = attraction.get_details()
        average_rating = attraction.get_average_rating()
        self.assertEquals(activity_title, "The pub")
        self.assertEquals(address, "London City")
        self.assertEquals(category, "restaurant")
        self.assertEquals(latitude, 1234554.0093)
        self.assertEquals(longitude, 123454325.653)
        self.assertEquals(average_rating, 60.0)
        self.assertEquals(details, "details")



    def test_shuffle(self):
        self.create_attraction_objects()
        self.assertTrue(Attraction.shuffle_attractions())

class TestReviewModel(TestCase):
    # class Review(models.Model):
    #     attraction = models.ForeignKey(Attraction, on_delete=models.CASCADE)  # - when we set up events
    #     user = models.ForeignKey(User, on_delete=models.CASCADE)  # The foreign key in this case is a User object
    #     review = models.CharField(max_length=100)
    #     sentiment = models.IntegerField()
    def test_create_review(self):
        TestAttractionModel().create_attraction_objects()
        TestUser().create_user()
        review = Review(1, 1, 1, "Best restaurant I have ever been to. Fantastic service and really great staff", 1)
        review.save()
        review_obj = Review.objects.get(pk=1)
        self.assertEquals(review_obj.get_review(), "Best restaurant I have ever been to. Fantastic service and really great staff")
        self.assertEquals(review_obj.get_user().id, 1)
        self.assertEquals(review_obj.get_attraction().id, 1)
        self.assertEquals(review_obj.get_sentiment(), 1)



class TestRatingModel(TestCase):
    # class Rating(models.Model):
    #     user = models.ForeignKey(User, on_delete=models.CASCADE)
    #     attraction = models.ForeignKey(Attraction, on_delete=models.CASCADE)
    #     rating = models.IntegerField(
    #         choices=rate_choices)  # Rating how liked or disliked an attraction is on a scale of 1-5
    #
    #     @staticmethod
    #     def get_rating_and_attraction_id(rating_and_id):
    #         rating_and_id = rating_and_id.split("+")
    #         rating_value = int(rating_and_id[0])
    #         attraction_id = int(rating_and_id[1])
    #         return rating_value, attraction_id
    def test_rating(self):
        TestAttractionModel().create_attraction_objects()
        TestUser().create_user()
        rating = Rating(1, 1, 2, 5)
        self.assertTrue(rating.get_rating(), 1)
        self.assertTrue(rating.get_user().id, 1)
        self.assertTrue(rating.get_attraction().id, 2)
        self.assertTrue(rating.get_rating(), 5)

    def test_get_rating_and_attraction_id(self):
        rating_and_attraction_id = "4+12"
        rating_value, attraction_id = Rating.split_rating_and_attraction_id(rating_and_attraction_id)
        self.assertEquals(rating_value, 4)
        self.assertEquals(attraction_id, 12)

class TestUserPreferencesModel(TestCase):
    # class
    # UserPreference(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE, unique=True, primary_key=True)
    #
    # attraction_preference_1 = models.CharField(choices=ATTRACTION_CHOICES, max_length=100)
    # attraction_preference_2 = models.CharField(choices=ATTRACTION_CHOICES, max_length=100)
    # attraction_preference_3 = models.CharField(choices=ATTRACTION_CHOICES, max_length=100)
    #
    # food_preference_1 = models.CharField(choices=FOOD_TYPE_CHOICES, max_length=100)
    # food_preference_2 = models.CharField(choices=FOOD_TYPE_CHOICES, max_length=100)
    # food_preference_3 = models.CharField(choices=FOOD_TYPE_CHOICES, max_length=100)
    def test_user_preferences(self):
        TestUser().create_user()
        user_preferences = UserPreference(1, 'chinese', 'thai', 'italian', 'park', 'animal-attraction', 'monument')
        user_preferences.save()
        user_pref = UserPreference.objects.get(pk=1)
        self.assertTrue(user_pref.attraction_preference_1, 'park')
        self.assertTrue(user_pref.attraction_preference_2, 'animal-attraction')
        self.assertTrue(user_pref.attraction_preference_3, 'theme-park')
        self.assertTrue(user_pref.food_preference_1, 'chinese')
        self.assertTrue(user_pref.food_preference_2, 'thai')
        self.assertTrue(user_pref.food_preference_3, 'italian')

class TestLocationModel(TestCase):

    def create_location(self):
        location = "London"
        pathToModel = "webapp/recommendation_engine/recommender_model.h5"
        model_location = Location(1, location, pathToModel)
        model_location.save()
        return model_location

    def test_model_location(self):
        location_obj = self.create_location()
        london_model = Location.objects.get(pk=1)
        self.assertEquals(london_model.get_location(), location_obj.get_location())
        self.assertEquals(london_model.get_path_to_model(), location_obj.get_path_to_model())


    # class Location(models.Model):
    #     location = models.CharField(max_length=100, null=True, blank=True)
    #     pathToModel = models.CharField(max_length=100)
    #
    #     def __str__(self):
    #         return f"{self.location}"

class TestTripModel(TestCase):

    def test_trip(self):
        TestUser().create_user()
        location = TestLocationModel().create_location()
        arrival_date = date(2022, 4, 29)
        departure_date = date(2022, 5, 10)
        trip = Trip(1, 1, arrival_date, departure_date)
        trip.save()

        user_trip = Trip.objects.get(pk=1)
        self.assertTrue(user_trip.get_location(), location)
        self.assertTrue(user_trip.get_arrival_date(), arrival_date)
        self.assertTrue(user_trip.get_departure_date(), departure_date)

    # LOCATION_CHOICES = [('London', "London")]
    #
    # class Trip(models.Model):
    #     user = models.ForeignKey(User, on_delete=models.CASCADE)
    #     location = models.ForeignKey(Location, on_delete=models.CASCADE)
    #     arrivalDate = models.DateField()
    #     departureDate = models.DateField()

class TestUser(TestCase):

    def create_user(self):
        user = User.objects.create_user(username="test1", email="test@gmail.com", password="test2022")
        user.save()
        return user

    def create_super_user(self):
        super_user = User.objects.create_superuser(username="supertest1", email="supertest@gmail.com", password="supertest2022")
        return super_user

    def test_User(self):
        user = self.create_user()
        self.assertEquals(user.username, "test1")
        self.assertEquals(user.email, "test@gmail.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_super_user(self):
        super_user = self.create_super_user()
        self.assertEquals(super_user.username, "supertest1")
        self.assertEquals(super_user.email, "supertest@gmail.com")
        self.assertTrue(super_user.is_active)
        self.assertTrue(super_user.is_staff)
        self.assertTrue(super_user.is_superuser)

    def test_create_user(self):
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(ValueError):
            User.objects.create_user(username="")
        with self.assertRaises(ValueError):
            User.objects.create_user(username="", email="test@gmail.com")
        with self.assertRaises(ValueError):
            User.objects.create_user(username="", email="test@gmail.com")