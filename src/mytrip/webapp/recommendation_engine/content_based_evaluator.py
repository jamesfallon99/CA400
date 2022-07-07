from content_based_evaluation_metrics import evaluation_metrics
from content_based_model import content_based_m

class evaluation(object):

    def __init__(self):
        pass
        self.evaluate = evaluation_metrics()
        self.content_based_mod = content_based_m("Potion Bar", 100)
        self.predictions = self.content_based_mod.get_predictions()

    def MAE(self):
        print(self.evaluate.MAE(self.predictions))

evaluation_met = evaluation_metrics()
evaluation_met.MAE()
