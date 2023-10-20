import numpy as np

from sklearn.metrics import balanced_accuracy_score

class ErrorMetric:
    
    @staticmethod
    def mse(true, pred):
        return np.mean([(t - p)**2 for t, p in zip(true, pred)])
    
    @staticmethod
    def rmse(true, pred):
        return np.sqrt(ErrorMetric.mse(true, pred))

    @staticmethod
    def balanced_error(true, pred):
        return 1 - balanced_accuracy_score(true, pred)
