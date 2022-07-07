import datetime
import tensorflow as tf
import pandas as pd
from keras.layers import Input, Embedding, Flatten, Dot, Dense, Concatenate, Reshape
from keras.models import Model
from sklearn.model_selection import train_test_split
import numpy as np

# read in csv files
ratings_df = pd.read_csv('recommendation_dataset/bias_ratings.csv')
activities_df = pd.read_csv('recommendation_dataset/recommendation_dataset.csv')

# do a train test split
train_ratings, test_ratings = train_test_split(ratings_df, test_size=0.2)
train_activities, test_activities = train_test_split(activities_df, test_size=0.2)

# gather unique user id's and map them to accending
users = ratings_df.userId.unique()
user_map = {i:val for i,val in enumerate(users)}
inverse_user_map = {val:i for i,val in enumerate(users)}
# gather unique activity id's and map them to accending
activities = ratings_df.activityId.unique()
activity_map = {i:val for i,val in enumerate(activities)}
inverse_activities_map = {val:i for i,val in enumerate(activities)}

ratings_df["userId"] = ratings_df["userId"].map(inverse_user_map)
ratings_df["activityId"] = ratings_df["activityId"].map(inverse_activities_map)

user_id_input = Input(shape=[1], name='user')
activity_id_input = Input(shape=[1], name='item')

embedding_size = 10
user_embedding = Embedding(output_dim=embedding_size, input_dim=users.shape[0], input_length=1, name='user_embedding')(user_id_input)
activity_embedding = Embedding(output_dim=embedding_size, input_dim=activities.shape[0], input_length=1, name='activity_embedding')(activity_id_input)

user_vecs = Reshape([embedding_size])(user_embedding)
activity_vecs = Reshape([embedding_size])(activity_embedding)
input_vecs = Concatenate()([user_vecs, activity_vecs])

x = Dense(128, activation='relu')(input_vecs)
x1 = Dense(64, activation='relu')(x)
x2 = Dense(32, activation='relu')(x1)

y = Dense(1)(x2)

model = Model(inputs=[user_id_input, activity_id_input], outputs=y)

model.compile(loss='mse',
              optimizer="adam"
             )

# train the model
# history = model.fit([train_ratings['userId'], train_ratings['activityId']],
#     train_ratings['ratings'],
#     batch_size=128,
#     epochs=3,
#     validation_split=0.2,
#     shuffle=True,
#     )

numUsers = pd.unique(ratings_df.userId)
numUsers = numUsers[:5]
numItems = ratings_df.activityId
numItems = numItems[:5]

print(numUsers, numItems)

# predictions = model.predict(
#     numUsers,
#     numItems,
#     verbose=0,
#     steps=None,
#     callbacks=None
# )
# # predictions = model.predict(samples_to_predict)
# print(predictions)
