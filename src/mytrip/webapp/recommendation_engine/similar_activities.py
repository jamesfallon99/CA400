from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sklearn.metrics.pairwise import cosine_similarity
from ..models import Attraction, SimilarAttractions

from .content_based_model import content_based_m
import pandas as pd

# Linked List class contains a Node object
class Dict:
 
    # Function to initialize head
    def __init__(self):
        self.dict = {}

    def add(self, k, v):
        self.dict[k] = v

    def remove(self, k):
        self.dict.pop(k)

    def print_items(self):
        self.dict.items()
 
# Code execution starts here
class SimActivities(object):
    # Start with the empty list

    def __init__(self):
        # similar_a = Dict()

        print('intialising model...')
        print('determining dataset...')
        self.rec_df = pd.read_csv('webapp/recommendation_dataset/production_dataframes/recommendation_dataset.csv', index_col=0)
        self.attraction_dataset = pd.read_csv('webapp/recommendation_dataset/production_dataframes/activity_features.csv', index_col=0)

    def recommedations_to_db(self):
        for index in self.rec_df.index[21389:]:
            recommendation_id = self.rec_df.loc[index, 'recommendation_id']
            model = content_based_m(recommendation_id, 12)
            print('getting predicitons for activity: ', recommendation_id)
            predictions = model.get_predictions()
            print(predictions)
            # similar_activities.add(activity_title, predicitons)
            activity = Attraction.objects.get(pk=recommendation_id)
            similar_attractions = SimilarAttractions(attraction=activity, similar_attraction1=predictions[1], similar_attraction2=predictions[2], similar_attraction3=predictions[3], similar_attraction4=predictions[4], similar_attraction5=predictions[5], similar_attraction6=predictions[6], similar_attraction7=predictions[7], similar_attraction8=predictions[8], similar_attraction9=predictions[9], similar_attraction10=predictions[10], similar_attraction11=predictions[11])
            similar_attractions.save()

    # print(similar_activities.print_items())
