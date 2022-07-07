from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ObjectDoesNotExist
from .models import ActivityFeatures, Review, Attraction, Trip, Location, Rating, UserPreference, SimilarAttractions
from .forms import CreateUserForm, CreateTripForm, UserInterestsForm, UserPreferenceForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from tensorflow.keras.preprocessing.text import Tokenizer
from django.contrib.auth.models import User
#from ..sentiment_analysis.sentiment_analysis import SentimentAnalysis
#from .sentiment_analysis_algorithm import SentimentAnalysis
from .csv_to_model import csv_datasets_to_models
from .sentiment_analysis import sentiment_analysis_algorithm
from .recommendation_engine.similar_activities import SimActivities
from .recommendation_engine import recommender
import time
# from asgiref.sync import sync_to_async


sentiment_analysis = sentiment_analysis_algorithm.SentimentAnalysis() #Creating sentiment_analysis object

# We need to preprocess the dataset the same way we did when we trained the model. This will ensure the most accurate results
preprocessed_reviews = sentiment_analysis.preprocess_reviews_dataframe(sentiment_analysis.df, 'review', 'preprocessed_review')  # Preprocessing the dataframe - lower casing, removing noise (html tags, numbers, special characters), removing stopwords

X = preprocessed_reviews['preprocessed_review'].values  # Recurrent neural networks require inputs in an array data type. Converting the preprocessed reviews into an array called X

tk = Tokenizer(
    lower=True)  # We need to initialise the tokeniser just like we did with the model. Here we are specifying that it should use lower case words when we tokenize our data in order to ensure consistency
tk.fit_on_texts(
    X)  # We fit the training data (preprocessed reviews stored in array X) on the tokenizer in order to tokenize our data into unique words.


@login_required(login_url="sign-in")
def view_event(request, id):
    if request.method == "POST": #two post requests can occur on this endpoint
        if 'rating' in request.POST:
            user_rating_value = request.POST.get('rating') #String value
            user_rating_value = int(user_rating_value) #we need to convert to an integer in order to store in the database


            try: #Check to see if the user has already rated this attraction
                rating = Rating.objects.get(user_id=request.user.id, attraction_id=id)
                rating.rating = user_rating_value
                rating.save() #if they have, update the object in the database

            except ObjectDoesNotExist: #Otherwise object doesn't exist and we create the object
                attraction = get_object_or_404(Attraction, pk=id)
                rating = Rating(user=request.user, attraction=attraction, rating=user_rating_value)

                rating.save()
            return redirect('current-trip')

        if 'review' in request.POST:# If a review is posted on an event, our goal is to predict the sentiment - whether the review is positive or negative (0 or 1 respectively)
            user_review = request.POST.get('review')  # Get the review from the review form on the event page
            review_pad = sentiment_analysis.preprocess_user_review(
                user_review, tk)  # Preprocess this review - using the same preprocessing techniques we used to build our model
            sentiment = sentiment_analysis.predict_sentiment(
                review_pad)  # Predict the sentiment using our semantic analysis machine learning model
            #print("sentiment:")
            #print(sentiment)
            attraction = get_object_or_404(Attraction, pk=id)
            #print(attraction.get_activity_title())
            sentiment_analysis.store_user_review_in_database(request, attraction, user_review, sentiment)  # Store the review in the database

            reviews = Review.objects.all().filter(
                attraction_id=attraction.id)  # getting all the Review objects associated with the attraction
            # As this occurs on a POST request, there will always be at least one review in the database for this event/attraction, therefore no need to handle with an exception
            average_sentiment_rating = sentiment_analysis.get_average_sentiment_rating(reviews)
            attraction.averageRating = average_sentiment_rating  # Updating the average rating associated with the attraction by setting the average rating to the averageRating field in our Attraction Model
            attraction.save()  # using save() to update the Attraction model in the database

    attraction = get_object_or_404(Attraction,
                                   pk=id)  # Will either get an Attraction object  with the given id, or it will return a 404 error in the browser
    try:
        reviews = Review.objects.all().filter(
            attraction_id=attraction.id)  # getting all the Review objects associated with the attraction
        # if there's no reviews, an empty list will be returned
        average_sentiment_rating = sentiment_analysis.get_average_sentiment_rating(reviews)  # Try to get the average sentiment

    except ZeroDivisionError:  # Catch the division by zero error if there are no reviews currently for that event/attraction
        return render(request, "webapp/event.html", {"attraction": attraction})

    return render(request, "webapp/event.html", {"attraction": attraction,
                                                 "rating": average_sentiment_rating})  # If successful in retrieving the reviews and getting the average sentiment rating, render the template


def welcome(request):

    return render(request, 'webapp/welcome.html')


@login_required(login_url="sign-in")
def home(request):
    # CsvToModel = csv_datasets_to_models.CsvToModel()
    # CsvToModel.create_activity_features_from_csv()
    # shuffled_attractions = shuffle_attractions()
    # print(shuffled_attractions)
    #user = User.objects.get(pk=6) #get a user object from database
    #print(user.id) #get the id from the user object
    # id = request.user.id
    # print(id)
    # user = User.objects.get(pk=id)
    # print(user.email)
    # print(user.username)
    # print(User.username)
    # create_ratings_from_csv()
    # create_users_from_csv()
    # get_attractions_from_csv()
    # create_user_preferences_from_csv()
    # similar_activities = SimActivities()
    # similar_activities.recommedations_to_db()

    return render(request, 'webapp/index.html')


@login_required(login_url="sign-in")
def create_trip(request):
    if request.method == "POST":
        location_id = request.POST.get('location')  # Getting the location primary key from the form
        location = Location.objects.get(
            pk=location_id)  # Using the primary key, to get the location object from the database
        path_to_model = location.pathToModel  # Get the recommendation model path location from the Location object e.g. "mytrip/london_model"
        arrival_date = request.POST.get('arrivalDate')
        departure_date = request.POST.get('departureDate')
        trip = Trip(user=request.user, location=location, arrivalDate=arrival_date,
                    departureDate=departure_date)
        trip.save()  # Once the trip has been created, we will redirect to the home page of their current trip. This will display the recommendations to the user in that location
        return redirect('current-trip')

    form = CreateTripForm()  # our customized form from forms.py
    context = {'form': form}
    return render(request, 'webapp/create-trip.html', context)

def highest_rated_items(user_id):
    rating_objects = Rating.objects.all().filter(user_id=user_id)
    rating_objects = sorted(rating_objects, key=lambda x: x.rating, reverse=True)
    # create function to get highest rated object from user's list of ratings
    # If a user has a long list of ratings, it would be better to have this value before they ever click on current trip
    # We would need to get the highest rated every time they rate an activity instead
    # attraction_id = 0
    # highest = 0
    # for item in rating_objects:
    #     print(item.rating)
    # print(rating_objects)
    # rating_objects.sort(reverse=True)
    # for rating_obj in rating_objects:
        # if rating_obj.rating > highest:
        #     highest = rating_obj.rating
        #     attraction_id = rating_obj.attraction_id
    return rating_objects[0], rating_objects[1], rating_objects[2]

@login_required(login_url="sign-in")
def current_trip(request):
    #We want to check if a trip already exists in the database for the user

    # try:
    #     reviews = Review.objects.all().filter(
    #         attraction_id=attraction_id)  # getting all the Review objects associated with the attraction
    #     # if there's no reviews, an empty list will be returned
    #     average_sentiment_rating = sentiment_analysis.get_average_sentiment_rating(reviews)  # Try to get the average sentiment

    # except ZeroDivisionError:  # Catch the division by zero error if there are no reviews currently for that event/attraction
    
    # content based content
    Trip.objects.get(pk=request.user.id)
    recommendation_set_1, recommendation_set_2, recommendation_set_3 =  highest_rated_items(request.user.id)
    activity_1 = recommendation_set_1.attraction
    activity_2 = recommendation_set_2.attraction
    activity_3 = recommendation_set_3.attraction


    activity_list = [activity_1, activity_2, activity_3]
    # print('Activity:', activity_id_3)

    # attraction_id = highest_rated_items(request.user.id)
    # attraction = Attraction.objects.get(pk=attraction_id)
    # print(attraction_id)
    # print(attraction.category)
    attraction_objects = []
    similar_attractions_ids = []
    activity_feature_objects = []
    for activity in activity_list:
        similar_attractions = SimilarAttractions.objects.get(pk=activity.id)
        similar_attractions_ids.append(similar_attractions.similar_attraction1)
        similar_attractions_ids.append(similar_attractions.similar_attraction2)
        similar_attractions_ids.append(similar_attractions.similar_attraction3)
        similar_attractions_ids.append(similar_attractions.similar_attraction4)
        similar_attractions_ids.append(similar_attractions.similar_attraction5)
        similar_attractions_ids.append(similar_attractions.similar_attraction6)
        similar_attractions_ids.append(similar_attractions.similar_attraction7)
        similar_attractions_ids.append(similar_attractions.similar_attraction8)
        similar_attractions_ids.append(similar_attractions.similar_attraction9)
        similar_attractions_ids.append(similar_attractions.similar_attraction10)
        similar_attractions_ids.append(similar_attractions.similar_attraction11)  

    # sentiment analysis and content based
    for attraction_id in similar_attractions_ids:
        reviews = Review.objects.all().filter(attraction_id=attraction_id)
        average_sentiment_rating = sentiment_analysis.get_average_sentiment_rating(reviews)  # Try to get the average sentiment
        attraction_objects.append((Attraction.objects.get(pk=attraction_id), average_sentiment_rating))
        activity_features = ActivityFeatures.objects.get(pk=attraction_id)
        activity_feature_objects.append(activity_features)
    #     print('activity objects: ', activity_features)
    # print('activity objects: ', activity_feature_objects)


    # for attraction in Attraction.objects.all():
    #     reviews = Review.objects.all().filter(attraction_id=attraction.id)
    #     average_sentiment_rating = sentiment_analysis.get_average_sentiment_rating(reviews)  # Try to get the average sentiment
    #     # attraction = Attraction.objects.get(pk=attraction_id)
    #     attraction.average_rating = average_sentiment_rating
    #     attraction.save()

    # # collaborative based filtering
    # # 1. predicting off h5 file
    # # bring list of predictions through
    # model = recommender.recommender(request.user.id,0, 12)
    # predictions = model.make_collaborative_based_predicitions()
    # print('predictions: ', predictions)
    # collaborative_based_objects = []
    # print('before')

    # print(Attraction.objects.get(pk=int(predictions[0])))
    # print(collaborative_based_objects)
    
    return render(request, 'webapp/current-trip.html', {"attractions": attraction_objects, "activityfeatures": activity_feature_objects})

# except (ObjectDoesNotExist, ZeroDivisionError):
#     no_current_trip = "You have no current trip, please create a trip in order to view your recommendations"
#     return render(request, 'webapp/current-trip.html', {'no_current_trip': no_current_trip})

# except (ZeroDivisionError):
#     print('zero devision error')


def registerPage(request):
    if request.user.is_authenticated:
        return redirect("home")
    else:
        if request.method == "POST":
            form = CreateUserForm(request.POST)

            if form.is_valid():
                form.save()
                messages.success(request, "Account Successfully Created for " + form.cleaned_data.get(
                    'username'))  # cleaned_data returns a dictionary of validated form input fields and their values. We are then accessing this dictionary to get the username
                return redirect("sign-in")
            else:
                return render(request, 'webapp/register.html', {
                    'form': form})  # need to render the template again as we use two different form instances for POST and GET requests
        form = CreateUserForm()  # our customized form from forms.py
        context = {'form': form}
        return render(request, 'webapp/register.html', context)


def sign_in(request):
    if request.user.is_authenticated:
        return redirect("home")
    else:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('user-interests')
            else:
                messages.info(request, 'Username or Password is incorrect')
        return render(request, 'webapp/sign-in.html')


def logoutUser(request):
    logout(request)
    return redirect("sign-in")

@login_required(login_url="sign-in")
def user_interests(request):

    if request.method == "POST": #If a user POSTs their activity ratings indicating their interest in a particular attraction/activity
        #if 'rating' in request.POST:
        i = 1
        while i <= 6: #Loop through all the ratings that were POSTed
            rating = request.POST.get('rating{}'.format(i)) #get the rating from the user-interest form
            rating_and_attraction_id = Rating.split_rating_and_attraction_id(rating) #split the rating and the attraction id into two tokens
            rating_value = rating_and_attraction_id[0] #assign the rating_value to a variable
            attraction_id = rating_and_attraction_id[1] #assign the attraction_id to a variable
            attraction = get_object_or_404(Attraction, pk=attraction_id) #get the attraction object from the database using the id as the primary key
            rating = Rating(user=request.user, attraction=attraction, rating=rating_value) #Create a Rating object
            rating.save() #save the Rating object to the database
            i += 1 #increase i to move onto the next rating

        # if 'attraction_preference_1' in request.POST:
        attraction_preference_1 = request.POST.get('attraction_preference_1')
        attraction_preference_2 = request.POST.get('attraction_preference_2')
        attraction_preference_3 = request.POST.get('attraction_preference_3')
        food_preference_1 = request.POST.get('food_preference_1')
        food_preference_2 = request.POST.get('food_preference_2')
        food_preference_3 = request.POST.get('food_preference_3')

        user_preference = UserPreference(user=request.user, food_preference_1=food_preference_1,
                                             food_preference_2=food_preference_2,
                                             food_preference_3=food_preference_3,
                                             attraction_preference_1=attraction_preference_1,
                                             attraction_preference_2=attraction_preference_2,
                                             attraction_preference_3=attraction_preference_3)
        user_preference.save()

        return redirect("home")

    userPreferenceForm = UserPreferenceForm()
    activity1, activity2, activity3, restaurant1, restaurant2, restaurant3 = Attraction.shuffle_attractions()
    print(activity1, activity2, activity3)

    return render(request, "webapp/user-interests.html", {"activity1": activity1, "activity2": activity2, "activity3": activity3, "restaurant1": restaurant1, "restaurant2": restaurant2, "restaurant3": restaurant3, "userPreferenceForm": userPreferenceForm})
