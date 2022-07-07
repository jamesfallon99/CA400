import pandas as pd
import random
import keras
import numpy as np
import tensorflow as tf
from keras import Input
from keras.layers.embeddings import Embedding
from keras.models import Sequential
from sklearn.model_selection import train_test_split
from keras.layers import Input, Embedding, Flatten, Dot, Dense, Concatenate
from keras.models import Model

class collab_based_model(object):

    # create model

    def __init__(self, userId, number_of_predictions):
    
        # read in up to date ratings data
        self.ratings = pd.read_csv('../recommendation_dataset/production_dataframes/final_ratings.csv', index_col=[0])
        self.train, self.test = train_test_split(self.ratings, test_size=0.2, random_state=42)

        # gather unique user id's and activity id's
        self.number_of_users = self.ratings.userId.nunique()
        self.number_of_activities = self.ratings.activityId.nunique()

        # # apply the mapping
        self.userId = userId
        self.number_of_predictions = number_of_predictions
        
        # self.model = keras.models.load_model("../recommendation_engine/recommendation_model.h5")
        self.model = self.create_model()

        # self.train_model()
        

        self.recommended_activity_ids = self.predict_recommendations()

    def create_model(self):
        activities_input = Input(shape=[1], name="Activity-Input")
        activities_embedding = Embedding(self.number_of_activities+1, 5, name="Activity-Embedding")(activities_input)
        activities_vec = Flatten(name="Flatten-Activities")(activities_embedding)

        user_input = Input(shape=[1], name="User-Input")
        user_embedding = Embedding(self.number_of_users+1, 5, name="User-Embedding")(user_input)
        user_vec = Flatten(name="Flatten-Users")(user_embedding)

        # hidden layers
        x = Dense(128, activation='relu')(activities_vec)
        x = Dense(64, activation='relu')(x)
        x = Dense(32, activation='relu')(x)

        # output layer
        activities_vec = Dense(1)(x)

        # hidden layers
        y = Dense(128, activation='relu')(user_vec)
        y = Dense(64, activation='relu')(y)
        y = Dense(32, activation='relu')(y)

        # output layer
        user_vec = Dense(1)(y)

        prod = Dot(name="Dot-Product", axes=1)([activities_vec, user_vec])
        model = Model([user_input, activities_input], prod)
        model.compile('adam', 'mean_squared_error')

        return model

    # train the model
    def train_model(self):
        history = self.model.fit([self.train.userId, self.train.activityId], self.train.ratings, batch_size = 64, epochs=1, verbose=1)    

    # save the model
    def save_model(self):
        self.model.save("recommender_model.h5")

    # def load_model(self):
    #     self.model = keras.models.load_model("webapp//recommendation_engine/recommendation_model.h5")

    # predict the recommendations
    def predict_recommendations(self):
        activity_data = np.array(list(set(self.ratings.activityId)))
        user2allattractions = np.array([self.userId for i in range(len(activity_data))])
        predictions = self.model.predict([user2allattractions, activity_data])
        predictions = np.array([a[0] for a in predictions])
        recommended_activity_ids = (-predictions).argsort()[:self.number_of_predictions]
        # print(recommended_activity_ids)
        recommended_activity_ids = recommended_activity_ids.tolist()
        return recommended_activity_ids

# model = collab_based_model(6, 10)
# predictions = model.predict_recommendations()
# print('predictions: ', predictions)
