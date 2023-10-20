import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


DATA = "X"
LABELS = "y"

TRAIN = "train"
TEST = "test"

FITNESS = "fitness"
PHENOTYPE = "phenotype"


def format_data(X, y):
    return {DATA: X, LABELS: y}

def bound_dataset(df: pd.DataFrame, astype=np.float32, precision=np.float32):
    return df.astype(astype).replace([np.nan, np.inf, -np.inf], [1, np.finfo(precision).max, np.finfo(precision).min])

def scale_data(train, test):
    sc = StandardScaler()
    train = bound_dataset(pd.DataFrame(sc.fit_transform(train))).to_numpy()
    test = bound_dataset(pd.DataFrame(sc.transform(test))).to_numpy()
    return train, test

def split_data(data: pd.DataFrame, seed):
        
    # Transform Data: This framework takes the first column as the label
    x, y = data[data.columns[1:]], data[data.columns[0]]

    # Split data (Train ~ 40% | Test ~ 20% | Validation ~ 40%) 
    X_train_validation, X_test, y_train_validation, y_test = train_test_split(x, y, test_size=0.2, random_state=seed)
    X_train, X_validation, y_train, y_validation = train_test_split(X_train_validation, y_train_validation, test_size=0.5, random_state=seed)

    return  format_data(pd.DataFrame(X_train.values, columns=X_train.columns), y_train),                                   \
            format_data(pd.DataFrame(X_test.values, columns=X_test.columns), y_test),                                      \
            format_data(pd.DataFrame(X_validation.values, columns=X_validation.columns), y_validation),                    \
            format_data(pd.DataFrame(X_train_validation.values, columns=X_train_validation.columns), y_train_validation)

def engineer_dataset(phenotype, data):
    """ Phenotype = Tuple: (Func1, Func2, ... , FuncN)"""
    # Dataset = Tuple: (pd.Series(NewFeature1), ..., pd.Series(NewFeatureN))
    new_dataset: tuple = eval(phenotype, globals(), {"x": data[DATA]})
    
    # Dataset = pd.DataFrame: [feature_1: pd.Series(NewFeature1), ... , feature_n: pd.Series(NewFeatureN)] 
    new_dataset: pd.DataFrame = pd.DataFrame({f"feature_{i}": series.to_list() for i, series in enumerate(new_dataset)})
    
    # Set min and max bounds
    new_dataset = bound_dataset(new_dataset, astype=np.float64)
    return format_data(new_dataset, data[LABELS])

def score(model, train, test, error_metric):
    # Scale Data
    X_train, X_test = scale_data(train[DATA], test[DATA])

    # Fit Model
    predictions = model.fit(X_train, train[LABELS]).predict(X_test)
    score = error_metric(test[LABELS], predictions)
    return score

def generate_grammar(max_features=10, operators=["+", "-", "*", "/"], df_columns=["c0", "c1", "c2"]):
    start = "<start> ::= <feature>," + "".join(["|<feature>" + ",<feature>"*i for i in range(1, max_features+1)])
    feature = "<feature> ::= <feature><op><feature> | (<feature><op><feature>) | x[<var>]"
    op = "<op> ::= " + "|".join(operators)
    var = "<var> ::= " + "|".join([f"'{col}'" if type(col) == str else str(col) for col in df_columns])
    return "\n".join([start, feature, op, var])
