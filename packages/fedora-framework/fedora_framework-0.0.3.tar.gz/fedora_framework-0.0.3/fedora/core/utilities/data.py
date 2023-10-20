import pandas as pd

class Data:
    
    @staticmethod
    def format(file, sep, label, index=None):
        df: pd.DataFrame = pd.read_csv(file, sep=sep, index_col=index)
        y = df.pop(label)
        return pd.concat([y, df], axis=1)
    
    @staticmethod
    def sklearn_format(dataset):
        df = pd.DataFrame(dataset.data)
        df.columns = [f"c{i}" for i in range(64)]
        y = pd.DataFrame(dataset.target)
        return pd.concat([y, df], axis=1)
    

    """ Datasets """
    
    @staticmethod
    def mnist():
        from sklearn.datasets import load_digits
        return Data.sklearn_format(load_digits())
