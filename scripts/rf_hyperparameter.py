#### selecet hyperparameters using bayesian optimization

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from bayes_opt import BayesianOptimization
from sklearn.model_selection import cross_val_score




#### Load processed data

final = pd.read_csv('final0204_orig.csv')
train_np = final.to_numpy()

#### split into train and test datasets
y = train_np[:,-1]
X = train_np[:, :-1]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

#### Define a objective function with the parameters that need to be optimized
def rf_cv(n_estimators, min_samples_split, max_features, max_depth):
    val = cross_val_score(
        RandomForestRegressor(n_estimators=int(n_estimators),
            min_samples_split=int(min_samples_split),
            max_features=min(max_features, 0.999), # float
            max_depth=int(max_depth),
            random_state=2
        ),
        X_train, y_train, scoring='r2', cv=5
    ).mean()
    return val
    
#### Run Bayesian optimization  
rf_bo = BayesianOptimization(
        rf_cv,
        {'n_estimators': (10, 250),
        'min_samples_split': (2, 25),
        'max_features': (0.1, 0.999),
        'max_depth': (5, 15)}
    )
    

rf_bo.probe(
    {'n_estimators': [100, 200, 300],
        'min_samples_split': [2, 10, 20],
        'max_features': [0.1, 0.5, 0.9],
        'max_depth': [10, 15,25]
    }
)


rf_bo.maximize()

#### output the optimal hyperparameters
rf_bo.max

#### print the cv score using optimal parameters
rf = RandomForestRegressor(max_depth=11, max_features=0.83, min_samples_split=4, n_estimators=111)
np.mean(cross_val_score(rf, X_train, y_train, cv=5, scoring='r2'))




