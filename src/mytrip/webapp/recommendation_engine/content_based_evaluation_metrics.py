from surprise import accuracy
from collections import defaultdict
from content_based_model import content_based_m
from sklearn.metrics.pairwise import linear_kernel

# create instance
# print("HR:        Hit Rate; how often we are able to recommend a left-out rating. Higher is better.")
# print("cHR:       Cumulative Hit Rate; hit rate, confined to ratings above a certain threshold. Higher is better.")
# print("ARHR:      Average Reciprocal Hit Rank - Hit rate that takes the ranking into account. Higher is better." )
# print("Coverage:  Ratio of users for whom recommendations above a certain threshold exist. Higher is better.")
# print("Diversity: 1-S, where S is the average similarity score between every possible pair of recommendations")
# print("           for a given user. Higher means more diverse.")
# print("Novelty:   Average popularity rank of recommended items. Higher means more novel.")

class evaluation_metrics(object):

    def __init__(self):
        pass

    def MAE(predictions):
        return accuracy.mae(predictions, verbose=False)

    # def RMSE(predictions):
    #     return accuracy.rmse(predictions, verbose=False)

    # def GetTopN(predictions, n=10, minimumRating=4.0):
    #     topN = defaultdict(list)

    #     for userID, movieID, actualRating, estimatedRating, _ in predictions:
    #             if (estimatedRating >= minimumRating):
    #                 topN[int(userID)].append((int(movieID), estimatedRating))

    #     for userID, ratings in topN.items():
    #         ratings.sort(key=lambda x: x[1], reverse=True)
    #         topN[int(userID)] = ratings[:n]

    #     return topN

    # def HitRate(topNPredicted, leftOutPredictions):
    #         hits = 0
    #         total = 0

    #         # For each left-out rating
    #         for leftOut in leftOutPredictions:
    #             userID = leftOut[0]
    #             leftOutMovieID = leftOut[1]
    #             # Is it in the predicted top 10 for this user?
    #             hit = False
    #             for movieID, predictedRating in topNPredicted[int(userID)]:
    #                 if (int(leftOutMovieID) == int(movieID)):
    #                     hit = True
    #                     break
    #             if (hit) :
    #                 hits += 1

    #             total += 1

    #         # Compute overall precision
    #         return hits/total
