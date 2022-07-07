import random
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Embedding
from tensorflow.keras.layers import LSTM
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pandas as pd
import spacy
import re
from tensorflow import keras
import numpy as np
#from mytrip.webapp.models import Review
from ..models import Attraction, Review


class SentimentAnalysis(object):

    def __init__(self):

        self.df = pd.read_csv(
        "webapp/sentiment_analysis/IMDBDataset.csv")  # To set up our initial semantic analysis model, we are using IMDB dataset which contains 50,000 reviews in english with a sentiment associated with each review (positive/negative)
        self.binary_sentiments = pd.read_csv(
        "webapp/sentiment_analysis/binary_sentiments.csv", index_col=[0])
        self.binary_sentiments.drop(self.binary_sentiments.filter(regex="Unname"),axis=1, inplace=True)
        self.nlp = spacy.load('en_core_web_lg')  # using spacy to load in the language library - here we are specifying to load the medium sized english library (we can use the large size if need be)
        self.stopwords = self.nlp.Defaults.stop_words  # spacy has a list of stopwords built in - we will use these in our preprocessing


    def preprocess_reviews_dataframe(self, df, review_field, preprocessed_review_field):
        df[preprocessed_review_field] = df[review_field].str.lower() #Lowering casing all reviews in the pandas dataframe and assigning it to a new column in the dataframe
        df[preprocessed_review_field] = df[preprocessed_review_field].apply(
            lambda review: re.sub(r"(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|http.+?", "", review)) #Pandas has a method apply() which allows you to pass a function and apply it on
        # every review in the pandas dataframe. Helps to preprocess data quickly and effieicntly and often used in machine learning . Learned here: https://www.geeksforgeeks.org/python-pandas-apply/#:~:text=03%20Jul%2C%202018-,Pandas.,data%20science%20and%20machine%20learning.
        #Learned how to use lambda here: https://realpython.com/python-lambda/ - lambda is an anonymous function e.g. lambda x: x + 1 is the equivilent to def add_one(x)
                                                                                                                                                                #return x + 1
        # Using a regular expression to remove numbers, HTML tags, and special characters
        #Used this site to help undertand how to use lambda functions https://stackoverflow.com/questions/47947438/preprocessing-string-data-in-pandas-dataframe
        df[preprocessed_review_field] = df[preprocessed_review_field].apply(lambda review: re.sub(r"\d+", "", review))

        df[preprocessed_review_field] = df[preprocessed_review_field].apply(
            lambda review: ' '.join([word for word in review.split() if word not in self.stopwords])) #Removing stopwords from the reviews using spacy's stopwords library

        return df #Once the preprocessing is complete, return the dataframe



    def binary_encode_sentiments(self, preprocessed_reviews_df):
        sentiment = {'positive': 1, #Creating a dictionary mapping the positive and negative to 0 and 1
                    'negative': 0}

        preprocessed_reviews_df['sentiment'] = [sentiment[item] for item in preprocessed_reviews_df['sentiment']] # Binary encoding all sentiments with 1 for positive and 0 for negative sentiments using a list comprehension

        return preprocessed_reviews_df



    def tokenize_and_sequence_data(self, preprocessed_reviews_df):
        X = preprocessed_reviews_df['preprocessed_review'].values #Recurrent neural networks require inputs in an array data type. Converting the preprocessed reviews into an array called X
        y = preprocessed_reviews_df['sentiment'].values #Converting the integer sentiments into an array called y.
        #These are both numpy arrays

        #For RNNs to work, all text data has to be integer encoded before it is fed in to the model. We used Keras' tokenizer.
        tk = Tokenizer(lower=True) #The tokenizer has to be initialised. Here we are specifying that it should use lower case words when we tokenize our data in order to ensure consistency
        tk.fit_on_texts(X) #We fit the training data (preprocessed reviews stored in array X) on the tokenizer in order to tokenize our data into unique words.
        #Once the data is fit, the tokenizer can be used to encode our reviews as it maps unique words to unique integers.
        X_seq = tk.texts_to_sequences(X) #using text_to_sequences, we convert our tokens into a sequence of integers (each integer representing a unique word)
        X_pad = pad_sequences(X_seq, maxlen=80, padding='post') #We then pad the sequences to ensure all reviews have the same length - this is very important for RNNs. It will pad any sequence less than 80 integers with 0s.Any sequence greater than 80 will be shortened to 80 integers

        return X_pad, y, len(tk.word_counts.keys())+1



    def train_model(self, X_pad, y, vocab_size):
        #Split the data into train and test data using sklearn's train_test_split. the test size will be 30% of the data
        X_train, X_test, y_train, y_test = train_test_split(X_pad, y, test_size=0.3, random_state=1)

        batch_size = 32
        vocabulary_size = vocab_size # embedding needs the size of the vocabulary. We get the length of the tokenizer word count and plus 1 to it
        max_words = 80 #Embedding needs the length of the input sequences (We used pad_sequences above to ensure sequences were only 80 integers in length)
        embedding_size = 32 #This specifies the amount of dimensions that will be used to represent each word. In deep learning the values often used are 50, 100, 300 but through trial and error 32 worked out well (this can still be refined more to get the right one for us)
        model = Sequential() #Creating our model
        model.add(Embedding(vocabulary_size, embedding_size, input_length=max_words))
        model.add(LSTM(200, dropout=0.2, recurrent_dropout=0.2))#adding 1 hidden Long short term memory (LSTM) layer with 200 memory cells. Refined this parameter to get better results. We used dropout to prevent overfitting (when a model learns the noise in the data and this negatively affects the model's prediction performance)
        model.add(Dense(1, activation='sigmoid')) #Use the sigmoid activation function in our output layer to predict the probability the review is positive or negative
        model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy']) #As we want to classify between positive and negative, we use binary-crossentropy

        model.fit(X_train, y_train, batch_size=batch_size, epochs=15, verbose=2)

        model.save("test.h5") #save the model

    def preprocess_user_review(self, user_review, tk):
        user_review_lower = user_review.lower()  # Converting the user review into lower case
        # will need to add preprocessing steps here - regular expressions to catch any noise in user reviews
        # For now, this will suffice
        user_review_denoised = " ".join([word for word in user_review_lower.split() if
                                         word not in self.stopwords])  # Removing stopwords from the user review
        list_of_user_review = []
        list_of_user_review.append(user_review_denoised)

        user_review_array = np.array(
            list_of_user_review)  # As RNNs need the input in an array, appending the user review into a numpy array
        review_seq = tk.texts_to_sequences(
            user_review_array)  # using text_to_sequences, we convert our tokens into a sequence of integers (each integer representing a unique word)
        review_pad = pad_sequences(review_seq, maxlen=80,
                                   padding='post')  # We then pad the sequences to ensure all reviews have the same length - we want to make sure the user review has been preprocessed the same as the model

        return review_pad

    def predict_sentiment(self, review_pad):
        sentiment_analysis_model = keras.models.load_model(
            "webapp/sentiment_analysis/test-for-web-app.h5")  # Loading our model from the file we saved when we created the model
        user_review_prediction = sentiment_analysis_model.predict(review_pad)  # Predict the sentiment
        check_user_review_prediction = np.where(user_review_prediction > 0.5, 1,
                                                0)  # If it's greater than 0.5, it's positive and if it's less than 0.5 it's negative
        sentiment = check_user_review_prediction[0][
            0]  # contained in a list in a numpy array so have to access it like so

        return sentiment

    def get_average_sentiment_rating(self, reviews):  # reviews is a list of Review objects from the database. A review object has an attribute "sentiment", we can therefore sum up the reviews with positive sentiments and get the average out of all the reviews.
        total_positives = 0
        total_reviews = 0

        for review in reviews:  # This is an O(n) approach, is there a faster more efficient way? Especially when there's a lot of reviews in the database (#Instead we could-> everytime we add a review to the database store a count of total reviews and how many have sentiment = 1 - this way we don't have to iterate through all reviews)
            if review.sentiment == 1:
                total_positives += 1
            total_reviews += 1

        average_rating = (total_positives / total_reviews) * 100
        average_rating = round(average_rating, 1)
        return average_rating

    def store_user_review_in_database(self, request, attraction, user_review, sentiment):
        review = Review(attraction=attraction, user=request.user, review=user_review,
                        sentiment=sentiment)  # Creating a review object (have to specify what columns as Django automatically sets the integer id)
        review.save()  # Inserting into the database

    def assign_attraction_to_review(self):
        recommendation_dataset = pd.read_csv('webapp/recommendation_dataset/production_dataframes/recommendation_dataset.csv')
        recommendation_dataset.drop(recommendation_dataset.loc[recommendation_dataset['category']=='poi'].index, inplace=True)
        recommendation_id_list = recommendation_dataset['recommendation_id'].tolist()

        i = 0
        for index in self.binary_sentiments.index:
            recommendation_ids_for_review = []
            recommendation_ids_for_review.append(random.choices(recommendation_id_list)[0])
            recommendation_ids_for_review.append(random.choices(recommendation_id_list)[0])
            recommendation_ids_for_review.append(random.choices(recommendation_id_list)[0])
            recommendation_ids_for_review.append(random.choices(recommendation_id_list)[0])
            recommendation_ids_for_review.append(random.choices(recommendation_id_list)[0])
            recommendation_ids_for_review.append(random.choices(recommendation_id_list)[0])
            recommendation_ids_for_review.append(random.choices(recommendation_id_list)[0])
            recommendation_ids_for_review.append(random.choices(recommendation_id_list)[0])
            recommendation_ids_for_review.append(random.choices(recommendation_id_list)[0])
            recommendation_ids_for_review.append(random.choices(recommendation_id_list)[0])
            recommendation_ids_string = ''
            for item in recommendation_ids_for_review:
                recommendation_ids_string += (str(item) + ' ')
            # print(recommendation_ids_string)

            # attraction = Attraction.objects.get(pk=recommendation_id)
            self.binary_sentiments.at[index, 'recommendation_id'] = recommendation_ids_string
            # print(self.binary_sentiments.at[index, 'recommendation_id'], i)
            # # new_ratings.at[index, 'ratings'] = randrange(1, 3)
            # i += 1
        print('yes')
        self.binary_sentiments.to_csv("webapp/sentiment_analysis/binary_sentiments.csv")


# sentiment_analysis = SentimentAnalysis()
# # sentiment_analysis.assign_attraction_to_review()
# preprocessed_reviews_df = sentiment_analysis.preprocess_reviews_dataframe(sentiment_analysis.df, "review", "preprocessed_review")
# preprocessed_reviews_df = sentiment_analysis.binary_encode_sentiments(preprocessed_reviews_df)
# # sentiment_analysis.binary_sentiments.insert(2, 'recommendation_id', range(2, len(sentiment_analysis.binary_sentiments) + 2))
# # sentiment_analysis.binary_sentiments.to_csv("webapp/sentiment_analysis/binary_sentiments.csv")
# tokenize_and_sequence = sentiment_analysis.tokenize_and_sequence_data(preprocessed_reviews_df)
# X_pad = tokenize_and_sequence[0]
# y = tokenize_and_sequence[1]
# vocab_size = tokenize_and_sequence[2]
# sentiment_analysis.train_model(X_pad, y, vocab_size)