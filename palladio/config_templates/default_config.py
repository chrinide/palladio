# Configuration file example for PALLADIO
# version: 2.0

import numpy as np

from sklearn.feature_selection import RFE
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC
from sklearn.model_selection import GridSearchCV

from palladio import datasets

import os

#####################
#   DATASET PATHS ###
#####################

# * All the path are w.r.t. config file path

# The list of all files required for the experiments

data_path = 'data/gedm.csv'
target_path = 'data/labels.csv'

# pandas.read_csv options
data_loading_options = {
    'delimiter': ',',
    'header': 0,
    'index_col': 0
}
target_loading_options = data_loading_options

try:
    dataset = datasets.load_csv(os.path.join(os.path.dirname(__file__),data_path),
                                os.path.join(os.path.dirname(__file__),target_path),
                                data_loading_options=data_loading_options,
                                target_loading_options=target_loading_options,
                                samples_on='col')
except:
    dataset = datasets.load_csv(os.path.join(os.path.dirname(__file__), 'data'),
                                os.path.join(os.path.dirname(__file__), 'labels'),
                                data_loading_options=data_loading_options,
                                target_loading_options=target_loading_options,
                                samples_on='col')


data, labels = dataset.data, dataset.target
feature_names = dataset.feature_names

#######################
#   SESSION OPTIONS ###
#######################

session_folder = 'palladio_test_session'

# The learning task, if None palladio tries to guess it
# [see sklearn.utils.multiclass.type_of_target]
learning_task = None

# The number of repetitions of 'regular' experiments
n_splits_regular = 50

# The number of repetitions of 'permutation' experiments
n_splits_permutation = 50

#######################
#  LEARNER OPTIONS  ###
#######################

# PIPELINE ###

# STEP 1: Variable selection
vs = RFE(LinearSVC(loss='hinge'), step=0.3)

# STEP 2: Classification
clf = LinearSVC(loss='hinge')

# COMPOSE THE PIPELINE
pipe = Pipeline([
    ('variable_selection', vs),
    ('classification', clf),
])


# Set the estimator to be a GridSearchCV
param_grid = {
    'variable_selection__n_features_to_select': [10, 20, 50],
    'variable_selection__estimator__C': np.logspace(-4, 0, 5),
}

estimator = GridSearchCV(pipe, param_grid=param_grid, cv=3, scoring='accuracy', n_jobs=1)

# Set options for ModelAssessment
ma_options = {
    'test_size': 0.25,
    'scoring': 'accuracy',
    'n_jobs': -1,
    'n_splits': n_splits_regular
}


# For the Pipeline object, indicate the name of the step from which to
# retrieve the list of selected features
# For a single estimator which has a `coef_` attributes (e.g., elastic net or
# lasso) set to True
vs_analysis = 'variable_selection'

# ~~ Signature Parameters ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
frequency_threshold = None

# ~~ Plotting Options ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
score_surfaces_options = {
    'logspace': ['variable_selection__C'],
    'plot_errors': True
}
