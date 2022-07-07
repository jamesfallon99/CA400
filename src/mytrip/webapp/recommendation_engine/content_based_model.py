import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
# import os
# path = os.getcwd()
    # return string from root

# ref - > https://github.com/pravinkumarosingh/MoRe/blob/main/movie_recommendation_system.ipynb

class content_based_m(object):
    
    def __init__(self, activity_user_likes, number_of_predictions):
        
        print('intialising model...')
        self.activity_user_likes = activity_user_likes
        self.number_of_predictions = number_of_predictions

        self.rec_df = pd.read_csv('webapp/recommendation_dataset/production_dataframes/recommendation_dataset.csv', index_col=0)

        print('determining dataset...')
        self.determine_dataset()

        self.cv = CountVectorizer()
        
        print('building matrix...')
        self.count_matrix = self.cv.fit_transform(self.attraction_dataset['combined_features'])

        print('calculating cosine similarity...')
        cosine_sim = cosine_similarity(self.count_matrix)

        self.activity_index = self.get_index_from_recommendation_id()

        self.similar_activities = list(enumerate(cosine_sim[self.activity_index]))

        self.sorted_similar_activities = sorted(self.similar_activities, key = lambda x:x[1], reverse = True)

        self.sorted_similar_activities = self.sorted_similar_activities[:number_of_predictions]

    def determine_dataset(self):
        print(self.activity_user_likes)
        # check which category is associated with the activity the user likes
        category = self.rec_df[self.rec_df.recommendation_id == self.activity_user_likes]["category"].values[0]
        print(category)
        if category == 'restaurant':
            self.attraction_dataset = pd.read_csv('webapp/recommendation_dataset/production_dataframes/restaurant_features.csv', index_col=0, nrows=20000)
        else:
            self.attraction_dataset = pd.read_csv('webapp/recommendation_dataset/production_dataframes/activity_features.csv', index_col=0)


    def get_index_from_recommendation_id(self):
        activity_index = self.attraction_dataset.index[self.attraction_dataset['recommendation_id']==self.activity_user_likes].values[0]
        return activity_index

    def get_predictions(self):
        print('making predictions...')
        predictions = self.sorted_similar_activities
        list_of_recommendation_ids = []
        i = 0
        while i < self.number_of_predictions:
            recommendation_id = self.attraction_dataset[self.attraction_dataset.index == (predictions[i][0])]["recommendation_id"].values[0]
            list_of_recommendation_ids.append(recommendation_id)
            i += 1
            # print(recommendation_id)
            combined_features = self.attraction_dataset.combined_features[self.attraction_dataset['recommendation_id']==recommendation_id].values[0]

        # print(list_of_recommendation_ids)
        return list_of_recommendation_ids

# model = content_based_m(25394, 11)
# predictions = model.get_predictions()
# print(predictions)



