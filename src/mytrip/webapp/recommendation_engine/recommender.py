from .content_based_model import content_based_m
from .collaborative_filtering_model import collab_based_model

# content_based_m = content_based_m("", 5)

class recommender(object):
    def __init__(self, userId, activity_title, number_of_predictions):
        self.userId = userId
        self.activity_title = activity_title
        self.number_of_predictions = number_of_predictions

    def make_content_based_predictions(self):
        content_based_mod = content_based_m(self.activity_title, self.number_of_predictions)
        predictions = content_based_mod.get_predictions()
        print('Predicitons for activity: ', self.activity_title, ', based on similar features: ')
        print(predictions)

    def make_collaborative_based_predicitions(self):
        collab_filtering_model = collab_based_model(self.userId, self.number_of_predictions)
        predictions = collab_filtering_model.predict_recommendations()
        return predictions
        # print('Predicitons for user: ', self.userId, ', based on what similar users also liked: ')
        # print(predictions)

    def user_predictions(self):
        content_based_predictions = self.make_content_based_predictions()
        collab_based_prediciton = self.make_collaborative_based_predicitions()

# generate_recommendation = recommender(3, "Potion Bar", 10)
# generate_recommendation.user_predictions()
