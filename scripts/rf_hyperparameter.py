#### selecet hyperparameters using grid search

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.model_selection import RandomizedSearchCV
from sklearn.model_selection import GridSearchCV

#### Load processed data

final = pd.read_csv('final0204_orig.csv')
train_np = final.to_numpy()

#### split into train and test datasets
y = train_np[:,-1]
X = train_np[:, :-1]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

#### set hyperparameters
n_estimators = [int(x) for x in range(100,1000,50)]
max_features = ['auto'] # Number of features to consider at every split
max_depth = [int(x) for x in range(10,100,10)] # Maximum number of levels in tree
max_depth.append(None)
min_samples_split = [2, 5, 10] # Minimum number of samples required to split a node
min_samples_leaf = [1, 2, 4]# Minimum number of samples required at each leaf node
bootstrap = [True] # Method of selecting samples for training each tree

#### create random grid
random_grid = {'n_estimators': n_estimators,
               'max_features': max_features,
               'max_depth': max_depth,
               'min_samples_split': min_samples_split,
               'min_samples_leaf': min_samples_leaf,
               'bootstrap': bootstrap}

rf = RandomForestRegressor()
#### Random search of parameters with 5-fold cross validation
rf_random = RandomizedSearchCV(estimator = rf, param_distributions = random_grid, n_iter = 100, cv = 5, verbose=2, random_state=42, n_jobs = -1)

#### fit the random search to the model
rf_random.fit(X_train, y_train)
rf_random.best_params_



