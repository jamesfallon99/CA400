from ..models import Attraction, Rating, Review, UserPreference, ActivityFeatures
import pandas as pd
from django.contrib.auth.models import User


class CsvToModel(object):
    def get_attractions_from_csv(self):  # This function is used to grab all the data from our recommendation_dataset and create Attraction objects from each row
        dataset = pd.read_csv("webapp/recommendation_dataset/production_dataframes/recommendation_dataset.csv")
        for row in dataset.itertuples():
            attraction = Attraction(id=row[3],
                                    activity_title=row[4],
                                    address=row[5],
                                    category=row[6],
                                    latitude=row[7],
                                    longitude=row[8],
                                    details=row[9])
            attraction.save()


    def create_users_from_csv(self):
        user_information = pd.read_csv("webapp/recommendation_engine/recommendation_dataset/pre-processing/user-information/userInformation.csv")
        for row in user_information.itertuples():
            user = User.objects.create_user(username=row[3], email=row[4], password=row[5])
            user.save()

    def create_ratings_from_csv(self):
        user_ratings = pd.read_csv("webapp/recommendation_engine/recommendation_dataset/production_dataframes/bias_ratings.csv")
        for row in user_ratings.itertuples():
            #get the user object using the id value from the csv file
            user_id = row[2]
            attraction_id = row[3]
            rating_value = row[4]
            user = User.objects.get(pk=user_id)
            attraction = Attraction.objects.get(pk=attraction_id)
            rating = Rating(user=user, attraction=attraction, rating=rating_value)

            rating.save()

    def create_user_preferences_from_csv(self):
        user_preferences = pd.read_csv("webapp/recommendation_engine/recommendation_dataset/pre-processing/user-information/userInformation.csv")
        i = 2
        for row in user_preferences.itertuples():
            user_preferences = row[6].split("|")
            user = User.objects.get(pk=i)
            user_pref = UserPreference(user=user, food_preference_1=user_preferences[0], food_preference_2=user_preferences[1], food_preference_3=user_preferences[2], attraction_preference_1=user_preferences[3], attraction_preference_2=user_preferences[4], attraction_preference_3=user_preferences[5])
            user_pref.save()
            i += 1



    def create_activity_features_from_csv(self):
        activity_features = pd.read_csv("webapp/recommendation_engine/recommendation_dataset/production_dataframes/activity_features.csv")
        for row in activity_features.itertuples():
            activity_id = row[3]
            activity = Attraction.objects.get(pk=activity_id)

            activity_features_list = Attraction.split_combined_features(row[4])

            activity_features_obj = ActivityFeatures(attraction=activity, feature1=activity_features_list[0], feature2=activity_features_list[1], feature3=activity_features_list[2], feature4=activity_features_list[3])
            activity_features_obj.save()


    def create_activity_features_from_csv(self):
        activity_features = pd.read_csv("webapp/recommendation_dataset/production_dataframes/activity_features.csv")
        for row in activity_features.itertuples():
            features = row[3].split(" ")
            activity = Attraction.objects.get(pk=int(row[2]))
            attraction_features = ActivityFeatures(activity=activity, feature1=features[0], feature2=features[1], feature3=features[2], feature4=features[3])
            attraction_features.save()

    def create_reviews_from_csv(self):
        review_dataset = pd.read_csv("webapp/sentiment_analysis/binary_sentiments.csv")
        for row in review_dataset.itertuples():
            recommendtion_id_list = row[3].split(" ")
            attraction1 = int(recommendtion_id_list[0])
            attraction2 = int(recommendtion_id_list[1])
            attraction3 = int(recommendtion_id_list[2])
            attraction4 = int(recommendtion_id_list[3])
            attraction5 = int(recommendtion_id_list[4])
            attraction6 = int(recommendtion_id_list[5])
            attraction7 = int(recommendtion_id_list[6])
            attraction8 = int(recommendtion_id_list[7])
            attraction9 = int(recommendtion_id_list[8])
            attraction10 = int(recommendtion_id_list[9])
            i = 0
            while i < 10:
                attraction = Attraction.objects.get(pk=int(recommendtion_id_list[i]))
                review = Review(attraction=attraction, review=row[4], sentiment=row[5])
                review.save()
                i += 1
            

    